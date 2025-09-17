#!/usr/bin/env python3
"""
词库管理API测试脚本
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def test_vocabulary_api():
    """测试词库管理API"""
    print("🧪 开始测试词库管理API...")
    print("=" * 50)
    
    # 测试获取词库列表
    print("\n1. 测试获取词库列表")
    try:
        response = requests.get(f"{BASE_URL}/vocabulary/libraries")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取词库列表成功")
            print(f"   词库数量: {len(data['data']['libraries'])}")
            for lib in data['data']['libraries']:
                print(f"   - {lib['name']}: {lib['groups_count']}个词组, {lib['total_words_count']}个单词")
        else:
            print(f"❌ 获取词库列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试获取词库详情
    print("\n2. 测试获取词库详情")
    try:
        response = requests.get(f"{BASE_URL}/vocabulary/libraries/1")
        if response.status_code == 200:
            data = response.json()
            library = data['data']
            print(f"✅ 获取词库详情成功")
            print(f"   词库名称: {library['name']}")
            print(f"   描述: {library['description']}")
            print(f"   标签: {library['tags']}")
            print(f"   难度等级: {library['difficulty_level']}")
        else:
            print(f"❌ 获取词库详情失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试获取词组列表
    print("\n3. 测试获取词组列表")
    try:
        response = requests.get(f"{BASE_URL}/vocabulary/libraries/1/groups")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取词组列表成功")
            print(f"   词组数量: {len(data['data']['groups'])}")
            for group in data['data']['groups']:
                print(f"   - {group['name']}: {group['words_count']}个单词")
        else:
            print(f"❌ 获取词组列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试获取单词列表
    print("\n4. 测试获取单词列表")
    try:
        response = requests.get(f"{BASE_URL}/vocabulary/groups/1/words")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取单词列表成功")
            print(f"   单词数量: {len(data['data']['words'])}")
            for word in data['data']['words']:
                print(f"   - {word['word']}: {word['translation']}")
        else:
            print(f"❌ 获取单词列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试搜索功能
    print("\n5. 测试搜索功能")
    try:
        response = requests.get(f"{BASE_URL}/vocabulary/libraries?search=小学")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 搜索功能正常")
            print(f"   搜索结果: {len(data['data']['libraries'])}个词库")
        else:
            print(f"❌ 搜索功能失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成！")

if __name__ == '__main__':
    test_vocabulary_api()