#!/usr/bin/env python3
"""
测试关卡API接口
"""
import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:5000/api"

def test_auth():
    """测试认证接口"""
    print("🔐 测试用户认证...")
    
    # 测试登录
    login_data = {
        "username": "demo",
        "password": "demo123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"登录状态: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ 登录成功，获取到token")
        return token
    else:
        print(f"❌ 登录失败: {response.text}")
        return None

def test_levels_api(token):
    """测试关卡API"""
    if not token:
        print("❌ 没有有效的token，跳过关卡API测试")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📋 测试关卡API...")
    
    # 测试获取关卡列表
    print("1. 测试获取关卡列表")
    response = requests.get(f"{BASE_URL}/levels/", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 成功获取关卡列表，共{len(data.get('data', {}).get('levels', []))}个关卡")
    else:
        print(f"   ❌ 获取关卡列表失败: {response.text}")
    
    # 测试获取用户进度
    print("\n2. 测试获取用户进度")
    response = requests.get(f"{BASE_URL}/levels/progress", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        progress = data.get('data', {})
        print(f"   ✅ 成功获取用户进度")
        print(f"   - 总关卡数: {progress.get('total_levels', 0)}")
        print(f"   - 已完成: {progress.get('completed_levels', 0)}")
        print(f"   - 总星数: {progress.get('total_stars', 0)}")
    else:
        print(f"   ❌ 获取用户进度失败: {response.text}")
    
    # 测试获取关卡详情
    print("\n3. 测试获取关卡详情")
    response = requests.get(f"{BASE_URL}/levels/1", headers=headers)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        level = data.get('data', {})
        print(f"   ✅ 成功获取关卡详情")
        print(f"   - 关卡标题: {level.get('title', 'N/A')}")
        print(f"   - 难度: {level.get('difficulty', 'N/A')}")
        print(f"   - 状态: {level.get('status', 'N/A')}")
    else:
        print(f"   ❌ 获取关卡详情失败: {response.text}")

def test_create_demo_user():
    """测试创建演示用户"""
    print("\n👤 测试创建演示用户...")
    
    user_data = {
        "username": "demo",
        "email": "demo@example.com",
        "password": "demo123",
        "nickname": "演示用户"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"注册状态: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ 演示用户创建成功")
    elif response.status_code == 400:
        print("ℹ️ 演示用户已存在")
    else:
        print(f"❌ 创建演示用户失败: {response.text}")

def main():
    """主测试函数"""
    print("🧪 开始测试关卡API接口")
    print("=" * 50)
    
    # 先尝试创建演示用户
    test_create_demo_user()
    
    # 测试认证
    token = test_auth()
    
    # 测试关卡API
    test_levels_api(token)
    
    print("\n" + "=" * 50)
    print("✅ 关卡API测试完成！")

if __name__ == '__main__':
    main()