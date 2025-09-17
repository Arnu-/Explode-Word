"""
用户相关API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.game import GameSession

users_bp = Blueprint('users', __name__)


@users_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取排行榜"""
    try:
        # 获取查询参数
        limit = request.args.get('limit', 10, type=int)
        sort_by = request.args.get('sort_by', 'best_score')  # best_score, total_wins, win_rate
        
        # 构建查询
        query = User.query.filter(User.total_games > 0)
        
        if sort_by == 'best_score':
            query = query.order_by(User.best_score.desc())
        elif sort_by == 'total_wins':
            query = query.order_by(User.total_wins.desc())
        elif sort_by == 'win_rate':
            # 按胜率排序，但要求至少玩过5局游戏
            query = query.filter(User.total_games >= 5).order_by(
                (User.total_wins * 100.0 / User.total_games).desc()
            )
        
        users = query.limit(limit).all()
        
        leaderboard = []
        for i, user in enumerate(users, 1):
            user_data = user.to_dict()
            user_data['rank'] = i
            leaderboard.append(user_data)
        
        return jsonify({
            'leaderboard': leaderboard,
            'sort_by': sort_by
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取排行榜失败: {str(e)}'}), 500


@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """获取用户统计信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取最近的游戏记录
        recent_sessions = GameSession.query.filter_by(
            user_id=user_id,
            status='finished'
        ).order_by(GameSession.finished_at.desc()).limit(10).all()
        
        recent_games = [session.to_dict() for session in recent_sessions]
        
        # 计算额外统计信息
        total_time = sum(session.time_used for session in recent_sessions)
        avg_time = total_time / len(recent_sessions) if recent_sessions else 0
        
        stats = {
            'user_info': user.to_dict(),
            'recent_games': recent_games,
            'additional_stats': {
                'average_time_per_game': round(avg_time, 2),
                'total_time_played': total_time,
                'games_this_week': len([
                    s for s in recent_sessions 
                    if s.finished_at and (datetime.utcnow() - s.finished_at).days <= 7
                ])
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'获取统计信息失败: {str(e)}'}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    """获取指定用户的公开信息"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 只返回公开信息
        user_info = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'total_games': user.total_games,
            'total_wins': user.total_wins,
            'best_score': user.best_score,
            'win_rate': user.win_rate,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        return jsonify({'user': user_info}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500


@users_bp.route('/search', methods=['GET'])
def search_users():
    """搜索用户"""
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'users': []}), 200
        
        # 搜索用户名或昵称
        users = User.query.filter(
            (User.username.contains(query)) | 
            (User.nickname.contains(query))
        ).limit(limit).all()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'avatar_url': user.avatar_url,
                'total_games': user.total_games,
                'best_score': user.best_score
            })
        
        return jsonify({'users': users_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'搜索用户失败: {str(e)}'}), 500