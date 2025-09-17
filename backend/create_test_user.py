#!/usr/bin/env python3
"""
创建测试用户脚本
"""
from app import create_app, db
from app.models.user import User

def create_test_user():
    """创建默认测试用户"""
    app = create_app()
    
    with app.app_context():
        # 检查是否已存在测试用户
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            print("测试用户 'admin' 已存在")
            print(f"用户名: admin")
            print(f"邮箱: {existing_user.email}")
            return
        
        # 创建测试用户
        test_user = User(
            username='admin',
            email='admin@explodeword.com',
            nickname='管理员'
        )
        test_user.set_password('123456')
        
        try:
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ 测试用户创建成功！")
            print("=" * 40)
            print("默认登录信息:")
            print("用户名: admin")
            print("密码: 123456")
            print("邮箱: admin@explodeword.com")
            print("昵称: 管理员")
            print("=" * 40)
            print("您现在可以使用这些信息登录系统")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建测试用户失败: {str(e)}")

if __name__ == '__main__':
    create_test_user()