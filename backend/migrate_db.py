#!/usr/bin/env python3
"""
数据库迁移脚本
用于在不同数据库类型之间迁移数据
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app import create_app, db
from app.models import User, Game, Word, WordCategory


def export_data():
    """导出当前数据库数据"""
    app = create_app()
    
    with app.app_context():
        print("正在导出数据...")
        
        # 导出用户数据
        users = User.query.all()
        users_data = [user.to_dict() for user in users]
        
        # 导出游戏配置
        games = Game.query.all()
        games_data = [game.to_dict() for game in games]
        
        # 导出单词分类
        categories = WordCategory.query.all()
        categories_data = [category.to_dict() for category in categories]
        
        # 导出单词数据
        words = Word.query.all()
        words_data = [word.to_dict(include_category=True, include_stats=True) for word in words]
        
        export_data = {
            'users': users_data,
            'games': games_data,
            'categories': categories_data,
            'words': words_data
        }
        
        # 保存到文件
        import json
        with open('database_export.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据导出完成！")
        print(f"用户数量: {len(users_data)}")
        print(f"游戏配置数量: {len(games_data)}")
        print(f"单词分类数量: {len(categories_data)}")
        print(f"单词数量: {len(words_data)}")
        print(f"导出文件: database_export.json")


def import_data():
    """导入数据到新数据库"""
    app = create_app()
    
    with app.app_context():
        print("正在导入数据...")
        
        # 读取导出文件
        import json
        try:
            with open('database_export.json', 'r', encoding='utf-8') as f:
                import_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 database_export.json 文件")
            return
        
        # 创建所有表
        db.create_all()
        
        # 导入单词分类
        print("导入单词分类...")
        for category_data in import_data.get('categories', []):
            if not WordCategory.query.filter_by(name=category_data['name']).first():
                category = WordCategory(
                    name=category_data['name'],
                    description=category_data['description'],
                    difficulty_level=category_data['difficulty_level']
                )
                db.session.add(category)
        
        db.session.commit()
        
        # 导入游戏配置
        print("导入游戏配置...")
        for game_data in import_data.get('games', []):
            if not Game.query.filter_by(name=game_data['name']).first():
                game = Game(
                    name=game_data['name'],
                    description=game_data['description'],
                    max_players=game_data['max_players'],
                    time_limit=game_data['time_limit'],
                    word_count=game_data['word_count'],
                    difficulty_level=game_data['difficulty_level']
                )
                game.set_rules_config(game_data.get('rules_config', {}))
                db.session.add(game)
        
        db.session.commit()
        
        # 导入单词数据
        print("导入单词数据...")
        for word_data in import_data.get('words', []):
            # 查找分类
            category = WordCategory.query.filter_by(name=word_data.get('category', {}).get('name')).first()
            if category and not Word.query.filter_by(word=word_data['word']).first():
                word = Word(
                    word=word_data['word'],
                    translation=word_data['translation'],
                    pronunciation=word_data.get('pronunciation'),
                    example_sentence=word_data.get('example_sentence'),
                    example_translation=word_data.get('example_translation'),
                    category_id=category.id,
                    difficulty_level=word_data['difficulty_level'],
                    usage_count=word_data.get('usage_count', 0),
                    correct_count=word_data.get('correct_count', 0)
                )
                db.session.add(word)
        
        db.session.commit()
        
        print("数据导入完成！")
        print(f"单词分类数量: {WordCategory.query.count()}")
        print(f"游戏配置数量: {Game.query.count()}")
        print(f"单词数量: {Word.query.count()}")


def migrate_database(from_type, to_type):
    """迁移数据库"""
    print(f"开始从 {from_type} 迁移到 {to_type}")
    
    # 设置源数据库
    os.environ['DATABASE_TYPE'] = from_type
    export_data()
    
    # 设置目标数据库
    os.environ['DATABASE_TYPE'] = to_type
    import_data()
    
    print("数据库迁移完成！")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法:")
        print("  python migrate_db.py export          # 导出当前数据库数据")
        print("  python migrate_db.py import          # 导入数据到当前数据库")
        print("  python migrate_db.py migrate sqlite mysql  # 从SQLite迁移到MySQL")
        print("  python migrate_db.py migrate mysql sqlite  # 从MySQL迁移到SQLite")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'export':
        export_data()
    elif command == 'import':
        import_data()
    elif command == 'migrate' and len(sys.argv) == 4:
        from_type = sys.argv[2]
        to_type = sys.argv[3]
        migrate_database(from_type, to_type)
    else:
        print("无效的命令参数")
        sys.exit(1)