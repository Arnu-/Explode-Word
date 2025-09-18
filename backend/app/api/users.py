"""
用户相关API
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
try:
    from app import db
    from app.models.user import User
    from app.models.game import GameSession
except ImportError:
    # 处理相对导入
    from ..models.user import User
    from ..models.game import GameSession
    from .. import db

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


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """获取用户完整档案信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取所有已完成的游戏记录
        all_sessions = GameSession.query.filter_by(
            user_id=user_id,
            status='finished'
        ).order_by(GameSession.finished_at.desc()).all()
        
        # 计算详细统计信息
        total_games = len(all_sessions)
        total_time = sum(session.time_used or 0 for session in all_sessions)
        total_correct = sum(session.correct_answers or 0 for session in all_sessions)
        total_wrong = sum(session.wrong_answers or 0 for session in all_sessions)
        
        # 计算平均准确率
        total_answers = total_correct + total_wrong
        avg_accuracy = round(total_correct / total_answers * 100, 1) if total_answers > 0 else 0
        
        # 计算连胜天数
        streak_days = calculate_streak_days(all_sessions)
        
        # 格式化游戏时长
        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        formatted_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        # 计算本周游戏数
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_games = len([
            s for s in all_sessions 
            if s.finished_at and s.finished_at >= week_ago
        ])
        
        # 计算平均分数
        avg_score = round(sum(s.final_score or 0 for s in all_sessions) / total_games) if total_games > 0 else 0
        
        # 获取最近20条游戏记录用于历史展示
        recent_sessions = all_sessions[:20]
        game_history = []
        
        for session in recent_sessions:
            # 判断游戏结果
            if session.accuracy >= 95:
                result = 'perfect'
                stars = 3
            elif session.accuracy >= 75:
                result = 'success'
                stars = 2 if session.accuracy >= 85 else 1
            else:
                result = 'failed'
                stars = 0
            
            game_history.append({
                'id': session.id,
                'levelId': session.game_id,
                'levelName': f'第{session.game_id}关：{session.game.name if session.game else "未知关卡"}',
                'mode': '挑战模式' if session.final_score > 400 else '训练模式',
                'score': session.final_score or 0,
                'duration': session.time_used or 0,
                'accuracy': session.accuracy,
                'result': result,
                'stars': stars,
                'playedAt': session.finished_at.isoformat() if session.finished_at else None
            })
        
        # 模拟成就系统
        achievements = [
            {
                'id': 1,
                'name': '初出茅庐',
                'description': '完成第一个关卡',
                'icon': 'fa-solid fa-star',
                'unlocked': total_games > 0
            },
            {
                'id': 2,
                'name': '词汇达人',
                'description': '累计答对100个单词',
                'icon': 'fa-solid fa-book',
                'unlocked': total_correct >= 100
            },
            {
                'id': 3,
                'name': '连胜王者',
                'description': '连续7天游戏',
                'icon': 'fa-solid fa-fire',
                'unlocked': streak_days >= 7
            },
            {
                'id': 4,
                'name': '完美主义',
                'description': '单关卡100%正确率',
                'icon': 'fa-solid fa-bullseye',
                'unlocked': any(s.accuracy == 100 for s in all_sessions)
            },
            {
                'id': 5,
                'name': '时间管理',
                'description': '在限定时间内完成关卡',
                'icon': 'fa-solid fa-stopwatch',
                'unlocked': any(s.time_used and s.time_used < 120 for s in all_sessions)
            },
            {
                'id': 6,
                'name': '收藏家',
                'description': '获得50颗星星',
                'icon': 'fa-solid fa-gem',
                'unlocked': sum(3 if s.accuracy >= 95 else (2 if s.accuracy >= 85 else (1 if s.accuracy >= 75 else 0)) for s in all_sessions) >= 50
            }
        ]
        
        profile_data = {
            'user_info': {
                **user.to_dict(),
                'level': min(42, max(1, total_games // 5 + 1)),  # 每5局游戏升1级
                'coins': user.total_score,  # 使用总分作为金币
                'completedLevels': len(set(s.game_id for s in all_sessions if s.game_id)),
                'totalStars': sum(3 if s.accuracy >= 95 else (2 if s.accuracy >= 85 else (1 if s.accuracy >= 75 else 0)) for s in all_sessions),
                'totalPlayTime': formatted_time,
                'accuracy': f"{avg_accuracy}%",
                'streak': streak_days
            },
            'game_history': game_history,
            'achievements': achievements,
            'statistics': {
                'weekly_games': weekly_games,
                'average_score': avg_score,
                'total_time_played': total_time,
                'total_correct_answers': total_correct,
                'total_wrong_answers': total_wrong
            }
        }
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户档案失败: {str(e)}'}), 500


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """更新用户档案信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        data = request.get_json()
        
        # 更新允许修改的字段
        if 'username' in data:
            # 检查用户名是否已存在
            existing_user = User.query.filter(
                User.username == data['username'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({'error': '用户名已存在'}), 400
            user.username = data['username']
        
        if 'email' in data:
            # 检查邮箱是否已存在
            existing_user = User.query.filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({'error': '邮箱已存在'}), 400
            user.email = data['email']
        
        if 'nickname' in data:
            user.nickname = data['nickname']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': '档案更新成功',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新档案失败: {str(e)}'}), 500


def calculate_streak_days(sessions):
    """计算连胜天数"""
    if not sessions:
        return 0
    
    # 按日期分组
    dates = set()
    for session in sessions:
        if session.finished_at:
            date = session.finished_at.date()
            dates.add(date)
    
    if not dates:
        return 0
    
    # 排序日期
    sorted_dates = sorted(dates, reverse=True)
    
    # 计算连续天数
    streak = 1
    current_date = sorted_dates[0]
    
    for i in range(1, len(sorted_dates)):
        expected_date = current_date - timedelta(days=i)
        if sorted_dates[i] == expected_date:
            streak += 1
        else:
            break
    
    return streak


@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """获取用户统计信息（简化版本）"""
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
        total_time = sum(session.time_used or 0 for session in recent_sessions)
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