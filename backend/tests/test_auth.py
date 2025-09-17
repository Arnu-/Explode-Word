"""
认证相关测试
"""
import json
import pytest
from app.models.user import User


class TestAuth:
    """认证测试类"""
    
    def test_register_success(self, client):
        """测试注册成功"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'nickname': '新用户'
        }
        
        response = client.post('/api/auth/register', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        result = json.loads(response.data)
        assert 'access_token' in result
        assert result['user']['username'] == 'newuser'
    
    def test_register_duplicate_username(self, client, test_user):
        """测试注册重复用户名"""
        data = {
            'username': 'testuser',  # 已存在的用户名
            'email': 'another@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert '用户名已存在' in result['error']
    
    def test_login_success(self, client, test_user):
        """测试登录成功"""
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'access_token' in result
        assert result['user']['username'] == 'testuser'
    
    def test_login_wrong_password(self, client, test_user):
        """测试登录密码错误"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401
        result = json.loads(response.data)
        assert '用户名或密码错误' in result['error']
    
    def test_get_profile_without_token(self, client):
        """测试未登录获取用户信息"""
        response = client.get('/api/auth/profile')
        assert response.status_code == 401
    
    def test_get_profile_with_token(self, client, test_user):
        """测试已登录获取用户信息"""
        # 先登录获取token
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        
        login_response = client.post('/api/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        
        token = json.loads(login_response.data)['access_token']
        
        # 使用token获取用户信息
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/auth/profile', headers=headers)
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['user']['username'] == 'testuser'