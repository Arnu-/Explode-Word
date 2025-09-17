#!/usr/bin/env python3
"""
初始化关卡数据脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.level import Level, LevelRecord
from app.models.user import User
from datetime import datetime

def init_levels():
    """初始化关卡数据"""
    app = create_app()
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 检查是否已有关卡数据
        if Level.query.first():
            print("关卡数据已存在，跳过初始化")
            return
        
        # 创建示例关卡
        levels_data = [
            {
                'title': '魔法森林挑战',
                'description': '在神秘的魔法森林中收集宝石，完成你的第一次冒险！',
                'difficulty': '简单',
                'estimated_time_minutes': 6,
                'max_score': 15000,
                'tasks_config': [
                    {'description': '收集至少15个魔法宝石', 'target': 15, 'type': 'collect'},
                    {'description': '在60秒内完成关卡', 'target': 60, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': None,
                'unlock_stars_required': 0,
                'reward_coins': 12450,
                'reward_exp': 100,
                'sort_order': 1
            },
            {
                'title': '水晶洞穴探险',
                'description': '深入水晶洞穴，寻找更多珍贵的宝石！',
                'difficulty': '简单',
                'estimated_time_minutes': 6,
                'max_score': 12000,
                'tasks_config': [
                    {'description': '收集至少10个魔法宝石', 'target': 10, 'type': 'collect'},
                    {'description': '在90秒内完成关卡', 'target': 90, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 1,
                'unlock_stars_required': 1,
                'reward_coins': 10800,
                'reward_exp': 120,
                'sort_order': 2
            },
            {
                'title': '古老遗迹挑战',
                'description': '探索古老的遗迹，面对更大的挑战！',
                'difficulty': '中等',
                'estimated_time_minutes': 7,
                'max_score': 18000,
                'tasks_config': [
                    {'description': '收集至少20个魔法宝石', 'target': 20, 'type': 'collect'},
                    {'description': '在120秒内完成关卡', 'target': 120, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 2,
                'unlock_stars_required': 2,
                'reward_coins': 11500,
                'reward_exp': 150,
                'sort_order': 3
            },
            {
                'title': '火山熔岩试炼',
                'description': '在危险的火山中证明你的勇气和技巧！',
                'difficulty': '中等',
                'estimated_time_minutes': 8,
                'max_score': 20000,
                'tasks_config': [
                    {'description': '收集至少25个魔法宝石', 'target': 25, 'type': 'collect'},
                    {'description': '在150秒内完成关卡', 'target': 150, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 3,
                'unlock_stars_required': 3,
                'reward_coins': 12450,
                'reward_exp': 180,
                'sort_order': 4
            },
            {
                'title': '冰雪王国征服',
                'description': '征服寒冷的冰雪王国，展现你的实力！',
                'difficulty': '中等',
                'estimated_time_minutes': 8,
                'max_score': 22000,
                'tasks_config': [
                    {'description': '收集至少30个魔法宝石', 'target': 30, 'type': 'collect'},
                    {'description': '在180秒内完成关卡', 'target': 180, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 4,
                'unlock_stars_required': 5,
                'reward_coins': 12450,
                'reward_exp': 200,
                'sort_order': 5
            },
            {
                'title': '暗影深渊挑战',
                'description': '进入危险的暗影深渊，面对终极挑战！',
                'difficulty': '困难',
                'estimated_time_minutes': 9,
                'max_score': 25000,
                'tasks_config': [
                    {'description': '收集至少35个魔法宝石', 'target': 35, 'type': 'collect'},
                    {'description': '在210秒内完成关卡', 'target': 210, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 5,
                'unlock_stars_required': 8,
                'reward_coins': 14800,
                'reward_exp': 250,
                'sort_order': 6
            },
            {
                'title': '龙族圣地',
                'description': '挑战传说中的龙族圣地，成为真正的英雄！',
                'difficulty': '困难',
                'estimated_time_minutes': 10,
                'max_score': 30000,
                'tasks_config': [
                    {'description': '收集至少40个魔法宝石', 'target': 40, 'type': 'collect'},
                    {'description': '在240秒内完成关卡', 'target': 240, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 6,
                'unlock_stars_required': 12,
                'reward_coins': 16000,
                'reward_exp': 300,
                'sort_order': 7
            },
            {
                'title': '终极试炼',
                'description': '最终的试炼等待着你，证明你是最强的冒险者！',
                'difficulty': '地狱',
                'estimated_time_minutes': 12,
                'max_score': 50000,
                'tasks_config': [
                    {'description': '收集至少50个魔法宝石', 'target': 50, 'type': 'collect'},
                    {'description': '在300秒内完成关卡', 'target': 300, 'type': 'time'},
                    {'description': '不损失任何生命值', 'target': 0, 'type': 'health'}
                ],
                'unlock_level_id': 7,
                'unlock_stars_required': 18,
                'reward_coins': 20000,
                'reward_exp': 500,
                'sort_order': 8
            }
        ]
        
        # 创建关卡
        created_levels = []
        for level_data in levels_data:
            level = Level(**level_data)
            level.set_tasks_config(level_data['tasks_config'])
            db.session.add(level)
            created_levels.append(level)
        
        # 提交到数据库
        db.session.commit()
        
        print(f"成功创建 {len(created_levels)} 个关卡")
        
        # 为第一个关卡设置正确的解锁关系
        for i, level in enumerate(created_levels):
            if i > 0:
                level.unlock_level_id = created_levels[i-1].id
        
        db.session.commit()
        print("关卡解锁关系设置完成")

def create_demo_user_records():
    """为演示用户创建一些游戏记录"""
    app = create_app()
    
    with app.app_context():
        # 查找演示用户（假设用户名为 demo）
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            print("未找到演示用户，跳过创建演示记录")
            return
        
        # 获取前几个关卡
        levels = Level.query.order_by(Level.sort_order).limit(6).all()
        
        # 为前3个关卡创建完成记录
        demo_records = [
            {
                'level_id': levels[0].id,
                'best_score': 12450,
                'stars': 3,
                'status': 'completed',
                'tasks_completion': [
                    {'completed': True, 'value': 18},
                    {'completed': False, 'value': 65},
                    {'completed': True, 'value': 0}
                ],
                'total_attempts': 2,
                'completed_attempts': 2,
                'best_time_seconds': 58,
                'last_played_at': datetime.utcnow(),
                'first_completed_at': datetime.utcnow()
            },
            {
                'level_id': levels[1].id,
                'best_score': 9820,
                'stars': 2,
                'status': 'completed',
                'tasks_completion': [
                    {'completed': True, 'value': 12},
                    {'completed': True, 'value': 85},
                    {'completed': False, 'value': 1}
                ],
                'total_attempts': 3,
                'completed_attempts': 2,
                'best_time_seconds': 82,
                'last_played_at': datetime.utcnow(),
                'first_completed_at': datetime.utcnow()
            },
            {
                'level_id': levels[2].id,
                'best_score': 7650,
                'stars': 1,
                'status': 'completed',
                'tasks_completion': [
                    {'completed': True, 'value': 22},
                    {'completed': False, 'value': 135},
                    {'completed': False, 'value': 2}
                ],
                'total_attempts': 4,
                'completed_attempts': 1,
                'best_time_seconds': 125,
                'last_played_at': datetime.utcnow(),
                'first_completed_at': datetime.utcnow()
            }
        ]
        
        # 为后面的关卡设置可用状态
        for i in range(3, min(6, len(levels))):
            demo_records.append({
                'level_id': levels[i].id,
                'status': 'available',
                'total_attempts': 0,
                'completed_attempts': 0
            })
        
        # 创建记录
        for record_data in demo_records:
            record = LevelRecord(user_id=demo_user.id, **record_data)
            if 'tasks_completion' in record_data:
                record.set_tasks_completion(record_data['tasks_completion'])
            db.session.add(record)
        
        db.session.commit()
        print(f"为用户 {demo_user.username} 创建了 {len(demo_records)} 条游戏记录")

if __name__ == '__main__':
    print("开始初始化关卡数据...")
    init_levels()
    create_demo_user_records()
    print("关卡数据初始化完成！")