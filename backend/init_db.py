#!/usr/bin/env python3
"""
数据库初始化脚本
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.game import Game
from app.models.word import Word, WordCategory

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建默认游戏配置
        if not Game.query.first():
            default_game = Game(
                name='经典单词爆炸',
                description='经典的单词翻译游戏，考验你的英语词汇量！',
                max_players=4,
                time_limit=300,  # 5分钟
                word_count=20,
                difficulty_level=1
            )
            
            default_game.set_rules_config({
                'scoring': {
                    'correct_answer': 10,
                    'wrong_answer': 0,
                    'time_bonus': True
                },
                'game_mode': 'classic',
                'allow_hints': True
            })
            
            db.session.add(default_game)
        
        # 创建默认单词分类
        if not WordCategory.query.first():
            categories = [
                WordCategory(name='日常用语', description='日常生活中常用的英语单词', difficulty_level=1),
                WordCategory(name='学习用品', description='学习和办公相关的英语单词', difficulty_level=1),
                WordCategory(name='食物饮料', description='食物和饮料相关的英语单词', difficulty_level=2),
                WordCategory(name='动物植物', description='动物和植物相关的英语单词', difficulty_level=2),
                WordCategory(name='科技数码', description='科技和数码产品相关的英语单词', difficulty_level=3),
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            
            # 获取分类ID
            daily_category = WordCategory.query.filter_by(name='日常用语').first()
            study_category = WordCategory.query.filter_by(name='学习用品').first()
            food_category = WordCategory.query.filter_by(name='食物饮料').first()
            
            # 创建示例单词
            sample_words = [
                # 日常用语
                Word(word='hello', translation='你好', category_id=daily_category.id, difficulty_level=1),
                Word(word='goodbye', translation='再见', category_id=daily_category.id, difficulty_level=1),
                Word(word='thank you', translation='谢谢', category_id=daily_category.id, difficulty_level=1),
                Word(word='please', translation='请', category_id=daily_category.id, difficulty_level=1),
                Word(word='sorry', translation='对不起', category_id=daily_category.id, difficulty_level=1),
                Word(word='excuse me', translation='打扰一下', category_id=daily_category.id, difficulty_level=1),
                Word(word='yes', translation='是的', category_id=daily_category.id, difficulty_level=1),
                Word(word='no', translation='不', category_id=daily_category.id, difficulty_level=1),
                Word(word='good morning', translation='早上好', category_id=daily_category.id, difficulty_level=1),
                Word(word='good night', translation='晚安', category_id=daily_category.id, difficulty_level=1),
                
                # 学习用品
                Word(word='book', translation='书', category_id=study_category.id, difficulty_level=1),
                Word(word='pen', translation='钢笔', category_id=study_category.id, difficulty_level=1),
                Word(word='pencil', translation='铅笔', category_id=study_category.id, difficulty_level=1),
                Word(word='paper', translation='纸', category_id=study_category.id, difficulty_level=1),
                Word(word='computer', translation='电脑', category_id=study_category.id, difficulty_level=1),
                Word(word='desk', translation='桌子', category_id=study_category.id, difficulty_level=1),
                Word(word='chair', translation='椅子', category_id=study_category.id, difficulty_level=1),
                Word(word='notebook', translation='笔记本', category_id=study_category.id, difficulty_level=1),
                Word(word='ruler', translation='尺子', category_id=study_category.id, difficulty_level=1),
                Word(word='eraser', translation='橡皮擦', category_id=study_category.id, difficulty_level=1),
                
                # 食物饮料
                Word(word='apple', translation='苹果', category_id=food_category.id, difficulty_level=1),
                Word(word='banana', translation='香蕉', category_id=food_category.id, difficulty_level=1),
                Word(word='water', translation='水', category_id=food_category.id, difficulty_level=1),
                Word(word='milk', translation='牛奶', category_id=food_category.id, difficulty_level=1),
                Word(word='bread', translation='面包', category_id=food_category.id, difficulty_level=1),
                Word(word='rice', translation='米饭', category_id=food_category.id, difficulty_level=1),
                Word(word='chicken', translation='鸡肉', category_id=food_category.id, difficulty_level=2),
                Word(word='fish', translation='鱼', category_id=food_category.id, difficulty_level=1),
                Word(word='vegetable', translation='蔬菜', category_id=food_category.id, difficulty_level=2),
                Word(word='fruit', translation='水果', category_id=food_category.id, difficulty_level=1),
            ]
            
            for word in sample_words:
                db.session.add(word)
        
        db.session.commit()
        print("数据库初始化完成！")
        print(f"游戏配置数量: {Game.query.count()}")
        print(f"单词分类数量: {WordCategory.query.count()}")
        print(f"单词数量: {Word.query.count()}")


if __name__ == '__main__':
    init_database()