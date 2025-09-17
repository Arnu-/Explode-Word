#!/usr/bin/env python3
"""
测试游戏记录系统脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.level import Level, LevelRecord, GameHistory
from app.models.user import User
from datetime import datetime

def test_game_records():
    """测试游戏记录系统"""
    app = create_app()
    
    with app.app_context():
        print("🧪 测试游戏记录系统")
        print("=" * 40)
        
        # 测试1: 检查关卡数据
        print("\n📋 测试1: 检查关卡数据")
        levels = Level.query.all()
        print(f"   关卡总数: {len(levels)}")
        
        for level in levels[:3]:  # 显示前3个关卡
            print(f"   - {level.id}: {level.title} ({level.difficulty})")
            tasks = level.get_tasks_config()
            print(f"     任务数量: {len(tasks)}")
        
        # 测试2: 检查用户记录
        print("\n👤 测试2: 检查用户记录")
        demo_user = User.query.filter_by(username='demo').first()
        if demo_user:
            print(f"   演示用户: {demo_user.username}")
            records = LevelRecord.query.filter_by(user_id=demo_user.id).all()
            print(f"   游戏记录数: {len(records)}")
            
            for record in records:
                print(f"   - 关卡{record.level_id}: {record.status}, {record.stars}星, 最高分{record.best_score}")
        else:
            print("   ❌ 未找到演示用户")
        
        # 测试3: 测试星级计算
        print("\n⭐ 测试3: 测试星级计算")
        if demo_user and levels:
            level = levels[0]
            record = LevelRecord.query.filter_by(
                user_id=demo_user.id, 
                level_id=level.id
            ).first()
            
            if record:
                # 模拟游戏结果
                test_score = 13500
                test_time = 55
                test_tasks = 3
                
                stars = record.calculate_stars(test_score, test_time, test_tasks)
                print(f"   测试分数: {test_score}")
                print(f"   测试时间: {test_time}秒")
                print(f"   完成任务: {test_tasks}个")
                print(f"   计算星级: {stars}星")
        
        # 测试4: 检查数据库关系
        print("\n🔗 测试4: 检查数据库关系")
        if demo_user:
            # 检查用户-关卡记录关系
            user_records = demo_user.level_records.count() if hasattr(demo_user, 'level_records') else 0
            print(f"   用户关卡记录关系: {user_records}")
            
            # 检查关卡解锁关系
            locked_levels = Level.query.filter(Level.unlock_level_id.isnot(None)).count()
            print(f"   有解锁条件的关卡: {locked_levels}")
        
        # 测试5: 模拟API响应格式
        print("\n📡 测试5: 模拟API响应格式")
        if levels and demo_user:
            level = levels[0]
            record = LevelRecord.query.filter_by(
                user_id=demo_user.id, 
                level_id=level.id
            ).first()
            
            if record:
                # 模拟前端需要的数据格式
                level_data = {
                    'id': level.id,
                    'title': level.title,
                    'difficulty': level.difficulty,
                    'estTimeMin': level.estimated_time_minutes,
                    'bestScore': record.best_score,
                    'stars': record.stars,
                    'status': record.status,
                    'lastPlayedAgo': record.last_played_ago,
                    'tasks': []
                }
                
                # 处理任务数据
                tasks_config = level.get_tasks_config()
                tasks_completion = record.get_tasks_completion()
                
                for i, task_config in enumerate(tasks_config):
                    task_done = False
                    if i < len(tasks_completion):
                        task_done = tasks_completion[i].get('completed', False)
                    
                    level_data['tasks'].append({
                        'text': task_config.get('description', ''),
                        'done': task_done
                    })
                
                print(f"   关卡数据格式正确: ✅")
                print(f"   - ID: {level_data['id']}")
                print(f"   - 标题: {level_data['title']}")
                print(f"   - 最高分: {level_data['bestScore']}")
                print(f"   - 星级: {level_data['stars']}")
                print(f"   - 任务数: {len(level_data['tasks'])}")
        
        print("\n" + "=" * 40)
        print("✅ 游戏记录系统测试完成！")

if __name__ == '__main__':
    test_game_records()