"""
游戏配置相关API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.game import Game

games_bp = Blueprint('games', __name__)


@games_bp.route('/', methods=['GET'])
def get_games():
    """获取游戏列表"""
    try:
        games = Game.query.filter_by(is_active=True).all()
        games_data = [game.to_dict() for game in games]
        
        return jsonify({'games': games_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏列表失败: {str(e)}'}), 500


@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """获取游戏详情"""
    try:
        game = Game.query.get(game_id)
        
        if not game:
            return jsonify({'error': '游戏不存在'}), 404
        
        return jsonify({'game': game.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏详情失败: {str(e)}'}), 500


@games_bp.route('/', methods=['POST'])
@jwt_required()
def create_game():
    """创建游戏配置（管理员功能）"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not all(k in data for k in ('name', 'description')):
            return jsonify({'error': '缺少必填字段'}), 400
        
        game = Game(
            name=data['name'],
            description=data['description'],
            max_players=data.get('max_players', 4),
            time_limit=data.get('time_limit', 300),
            word_count=data.get('word_count', 20),
            difficulty_level=data.get('difficulty_level', 1)
        )
        
        # 设置规则配置
        if 'rules_config' in data:
            game.set_rules_config(data['rules_config'])
        
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'message': '游戏创建成功',
            'game': game.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建游戏失败: {str(e)}'}), 500


@games_bp.route('/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    """更新游戏配置（管理员功能）"""
    try:
        game = Game.query.get(game_id)
        
        if not game:
            return jsonify({'error': '游戏不存在'}), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'name' in data:
            game.name = data['name']
        if 'description' in data:
            game.description = data['description']
        if 'max_players' in data:
            game.max_players = data['max_players']
        if 'time_limit' in data:
            game.time_limit = data['time_limit']
        if 'word_count' in data:
            game.word_count = data['word_count']
        if 'difficulty_level' in data:
            game.difficulty_level = data['difficulty_level']
        if 'rules_config' in data:
            game.set_rules_config(data['rules_config'])
        if 'is_active' in data:
            game.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': '游戏更新成功',
            'game': game.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新游戏失败: {str(e)}'}), 500


@games_bp.route('/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    """删除游戏配置（管理员功能）"""
    try:
        game = Game.query.get(game_id)
        
        if not game:
            return jsonify({'error': '游戏不存在'}), 404
        
        # 软删除：设置为不活跃
        game.is_active = False
        db.session.commit()
        
        return jsonify({'message': '游戏删除成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除游戏失败: {str(e)}'}), 500