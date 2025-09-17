"""
认证相关API
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': '缺少必填字段'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # 验证数据格式
        if not validate_email(email):
            return jsonify({'error': '邮箱格式不正确'}), 400
        
        if not validate_password(password):
            return jsonify({'error': '密码长度至少6位'}), 400
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '邮箱已被注册'}), 400
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            nickname=data.get('nickname', username)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # 生成访问令牌
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        if not all(k in data for k in ('username', 'password')):
            return jsonify({'error': '缺少用户名或密码'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # 查找用户（支持用户名或邮箱登录）
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成访问令牌
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        data = request.get_json()
        
        # 更新允许修改的字段
        if 'nickname' in data:
            user.nickname = data['nickname'].strip()
        
        if 'avatar_url' in data:
            user.avatar_url = data['avatar_url']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': '更新成功',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        data = request.get_json()
        
        if not all(k in data for k in ('old_password', 'new_password')):
            return jsonify({'error': '缺少必填字段'}), 400
        
        old_password = data['old_password']
        new_password = data['new_password']
        
        # 验证旧密码
        if not user.check_password(old_password):
            return jsonify({'error': '原密码错误'}), 400
        
        # 验证新密码
        if not validate_password(new_password):
            return jsonify({'error': '新密码长度至少6位'}), 400
        
        # 更新密码
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'密码修改失败: {str(e)}'}), 500