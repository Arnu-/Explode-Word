#!/usr/bin/env python3
"""
游戏数据设置脚本 - 一键初始化所有游戏相关数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_demo_user import create_demo_user
from init_levels import init_levels, create_demo_user_records

def main():
    """主函数 - 按顺序执行所有初始化步骤"""
    print("=" * 50)
    print("🎮 Explode Word 游戏数据初始化")
    print("=" * 50)
    
    try:
        # 步骤1: 创建演示用户
        print("\n📝 步骤1: 创建演示用户...")
        create_demo_user()
        
        # 步骤2: 初始化关卡数据
        print("\n🏰 步骤2: 初始化关卡数据...")
        init_levels()
        
        # 步骤3: 创建演示用户的游戏记录
        print("\n🎯 步骤3: 创建演示游戏记录...")
        create_demo_user_records()
        
        print("\n" + "=" * 50)
        print("✅ 游戏数据初始化完成！")
        print("=" * 50)
        print("\n📋 初始化内容:")
        print("   • 创建演示用户 (用户名: demo, 密码: demo123)")
        print("   • 创建8个示例关卡")
        print("   • 为演示用户创建游戏记录")
        print("\n🚀 现在可以启动前端和后端服务进行测试！")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()