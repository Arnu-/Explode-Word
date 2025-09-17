#!/usr/bin/env python3
"""
创建演示用户脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User

def create_demo_user():
    """创建演示用户"""
    app = create_app()
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 检查是否已有演示用户
        demo_user = User.query.filter_by(username='demo').first()
        if demo_user:
            print("演示用户已存在")
            return demo_user
        
        # 创建演示用户
        demo_user = User(
            username='demo',
            email='demo@example.com',
            nickname='演示用户',
            total_games=5,
            total_wins=3,
            best_score=12450,
            total_score=35000
        )
        demo_user.set_password('demo123')
        
        db.session.add(demo_user)
        db.session.commit()
        
        print(f"成功创建演示用户: {demo_user.username}")
        return demo_user

if __name__ == '__main__':
    create_demo_user()