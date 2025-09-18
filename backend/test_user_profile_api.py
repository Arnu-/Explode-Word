#!/usr/bin/env python3
"""
测试用户档案API
"""
import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:5000/api"

def test_user_profile_api():
    """测试用户档案相关API"""
    
    print("🚀 开始测试用户档案API...")
    
    # 1. 测试用户注册
    print("\n1. 测试用户注册...")
    register_data = {
        "username": "testuser_profile",
        "email": "testuser_profile@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"注册响应状态: {response.status_code}")
        if response.status_code == 201:
            print("✅ 用户注册成功")
        elif response.status_code == 400:
            print("⚠️ 用户可能已存在，继续测试...")
        else:
            print(f"❌ 注册失败: {response.text}")
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
    
    # 2. 测试用户登录
    print("\n2. 测试用户登录...")
    login_data = {
        "username": "testuser_profile",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"登录响应状态: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            access_token = login_result.get('access_token')
            print("✅ 用户登录成功")
            print(f"Token: {access_token[:50]}...")
            
            # 设置认证头
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # 3. 测试获取用户档案
            print("\n3. 测试获取用户档案...")
            try:
                response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
                print(f"获取档案响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    profile_data = response.json()
                    print("✅ 获取用户档案成功")
                    print(f"用户信息: {json.dumps(profile_data.get('user_info', {}), indent=2, ensure_ascii=False)}")
                    print(f"游戏历史记录数量: {len(profile_data.get('game_history', []))}")
                    print(f"成就数量: {len(profile_data.get('achievements', []))}")
                else:
                    print(f"❌ 获取档案失败: {response.text}")
            except Exception as e:
                print(f"❌ 获取档案请求失败: {e}")
            
            # 4. 测试更新用户档案
            print("\n4. 测试更新用户档案...")
            update_data = {
                "nickname": "测试昵称",
                "username": "testuser_profile_updated"
            }
            
            try:
                response = requests.put(f"{BASE_URL}/users/profile", json=update_data, headers=headers)
                print(f"更新档案响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    update_result = response.json()
                    print("✅ 更新用户档案成功")
                    print(f"更新后用户信息: {json.dumps(update_result.get('user', {}), indent=2, ensure_ascii=False)}")
                else:
                    print(f"❌ 更新档案失败: {response.text}")
            except Exception as e:
                print(f"❌ 更新档案请求失败: {e}")
            
            # 5. 测试获取用户统计
            print("\n5. 测试获取用户统计...")
            try:
                response = requests.get(f"{BASE_URL}/users/stats", headers=headers)
                print(f"获取统计响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    stats_data = response.json()
                    print("✅ 获取用户统计成功")
                    print(f"统计信息: {json.dumps(stats_data.get('additional_stats', {}), indent=2, ensure_ascii=False)}")
                else:
                    print(f"❌ 获取统计失败: {response.text}")
            except Exception as e:
                print(f"❌ 获取统计请求失败: {e}")
            
        else:
            print(f"❌ 登录失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
    
    print("\n🎉 用户档案API测试完成!")

if __name__ == "__main__":
    test_user_profile_api()