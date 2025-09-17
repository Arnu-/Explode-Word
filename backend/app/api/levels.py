"""
关卡和游戏记录相关API
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.level import Level, LevelRecord, GameHistory
from app.models.user import User

levels_bp = Blueprint('levels', __name__)


@levels_bp.route('/', methods=['GET'])
@jwt_required()
def get_levels():
    """获取关卡列表（包含用户记录）"""
    try:
        user_id = int(get_jwt_identity())
        
        # 获取所有活跃关卡
        levels = Level.query.filter_by(is_active=True).order_by(Level.sort_order).all()
        
        # 获取用户的关卡记录
        user_records = {
            record.level_id: record 
            for record in LevelRecord.query.filter_by(user_id=user_id).all()
        }
        
        levels_data = []
        for level in levels:
            level_dict = level.to_dict()
            
            # 添加用户记录信息
            if level.id in user_records:
                record = user_records[level.id]
                level_dict.update({
                    'best_score': record.best_score,
                    'stars': record.stars,
                    'status': record.status,
                    'tasks_completion': record.get_tasks_completion(),
                    'last_played_ago': record.last_played_ago,
                    'total_attempts': record.total_attempts,
                    'completed_attempts': record.completed_attempts,
                    'completion_rate': record.completion_rate
                })
            else:
                # 默认状态
                level_dict.update({
                    'best_score': None,
                    'stars': 0,
                    'status': 'locked' if level.unlock_level_id else 'available',
                    'tasks_completion': [],
                    'last_played_ago': '—',
                    'total_attempts': 0,
                    'completed_attempts': 0,
                    'completion_rate': 0
                })
            
            # 处理任务数据格式，匹配前端需求
            tasks_config = level.get_tasks_config()
            tasks_completion = level_dict['tasks_completion']
            
            level_dict['tasks'] = []
            for i, task_config in enumerate(tasks_config):
                task_done = False
                if i < len(tasks_completion):
                    task_done = tasks_completion[i].get('completed', False)
                
                level_dict['tasks'].append({
                    'text': task_config.get('description', ''),
                    'done': task_done
                })
            
            # 映射字段名以匹配前端
            level_dict['estTimeMin'] = level_dict['estimated_time_minutes']
            level_dict['lastPlayedAgo'] = level_dict['last_played_ago']
            
            levels_data.append(level_dict)
        
        return jsonify({'levels': levels_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取关卡列表失败: {str(e)}'}), 500


@levels_bp.route('/<int:level_id>', methods=['GET'])
@jwt_required()
def get_level_detail(level_id):
    """获取关卡详情"""
    try:
        user_id = get_jwt_identity()
        
        level = Level.query.get(level_id)
        if not level or not level.is_active:
            return jsonify({'error': '关卡不存在'}), 404
        
        # 获取用户记录
        record = LevelRecord.query.filter_by(
            user_id=user_id, 
            level_id=level_id
        ).first()
        
        level_data = level.to_dict()
        
        if record:
            level_data.update({
                'user_record': record.to_dict()
            })
        else:
            level_data.update({
                'user_record': None
            })
        
        return jsonify({'level': level_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取关卡详情失败: {str(e)}'}), 500


@levels_bp.route('/<int:level_id>/start', methods=['POST'])
@jwt_required()
def start_level(level_id):
    """开始关卡游戏"""
    try:
        user_id = get_jwt_identity()
        
        level = Level.query.get(level_id)
        if not level or not level.is_active:
            return jsonify({'error': '关卡不存在'}), 404
        
        # 获取或创建用户记录
        record = LevelRecord.query.filter_by(
            user_id=user_id, 
            level_id=level_id
        ).first()
        
        if not record:
            record = LevelRecord(
                user_id=user_id,
                level_id=level_id,
                status='available'
            )
            db.session.add(record)
        
        # 检查解锁条件
        if record.status == 'locked':
            return jsonify({'error': '关卡尚未解锁'}), 400
        
        # 增加尝试次数
        record.total_attempts += 1
        record.last_played_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': '关卡开始',
            'level': level.to_dict(),
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'开始关卡失败: {str(e)}'}), 500


@levels_bp.route('/<int:level_id>/complete', methods=['POST'])
@jwt_required()
def complete_level(level_id):
    """完成关卡"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        level = Level.query.get(level_id)
        if not level or not level.is_active:
            return jsonify({'error': '关卡不存在'}), 404
        
        # 验证必填字段
        required_fields = ['score', 'time_seconds', 'correct_answers', 'wrong_answers', 'tasks_result']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必填字段'}), 400
        
        # 获取用户记录
        record = LevelRecord.query.filter_by(
            user_id=user_id, 
            level_id=level_id
        ).first()
        
        if not record:
            return jsonify({'error': '请先开始关卡'}), 400
        
        score = data['score']
        time_seconds = data['time_seconds']
        tasks_result = data['tasks_result']
        
        # 计算任务完成数量
        tasks_completed = sum(1 for task in tasks_result if task.get('completed', False))
        
        # 计算星级
        stars_earned = record.calculate_stars(score, time_seconds, tasks_completed)
        
        # 检查是否创造新纪录
        is_new_record = False
        if score > record.best_score:
            record.best_score = score
            is_new_record = True
        
        # 更新最佳时间
        if not record.best_time_seconds or time_seconds < record.best_time_seconds:
            record.best_time_seconds = time_seconds
        
        # 更新星级（取最高值）
        if stars_earned > record.stars:
            record.stars = stars_earned
        
        # 更新任务完成状态
        record.set_tasks_completion(tasks_result)
        
        # 更新记录状态
        record.completed_attempts += 1
        record.total_time_seconds += time_seconds
        record.status = 'completed'
        
        if not record.first_completed_at:
            record.first_completed_at = datetime.utcnow()
        
        # 创建游戏历史记录
        history = GameHistory(
            user_id=user_id,
            level_id=level_id,
            score=score,
            time_seconds=time_seconds,
            stars_earned=stars_earned,
            correct_answers=data['correct_answers'],
            wrong_answers=data['wrong_answers'],
            total_questions=data['correct_answers'] + data['wrong_answers'],
            is_completed=True,
            is_new_record=is_new_record
        )
        history.set_tasks_result(tasks_result)
        
        db.session.add(history)
        
        # 更新用户总体统计
        user = User.query.get(user_id)
        user.total_score += score
        if score > user.best_score:
            user.best_score = score
        
        # 检查并解锁下一关卡
        next_levels = Level.query.filter_by(unlock_level_id=level_id).all()
        unlocked_levels = []
        
        for next_level in next_levels:
            # 检查星星数量要求
            user_total_stars = db.session.query(db.func.sum(LevelRecord.stars)).filter_by(user_id=user_id).scalar() or 0
            
            if user_total_stars >= next_level.unlock_stars_required:
                next_record = LevelRecord.query.filter_by(
                    user_id=user_id, 
                    level_id=next_level.id
                ).first()
                
                if not next_record:
                    next_record = LevelRecord(
                        user_id=user_id,
                        level_id=next_level.id,
                        status='available'
                    )
                    db.session.add(next_record)
                elif next_record.status == 'locked':
                    next_record.status = 'available'
                
                unlocked_levels.append(next_level.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'message': '关卡完成',
            'score': score,
            'stars_earned': stars_earned,
            'is_new_record': is_new_record,
            'record': record.to_dict(),
            'unlocked_levels': unlocked_levels
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'完成关卡失败: {str(e)}'}), 500


@levels_bp.route('/history', methods=['GET'])
@jwt_required()
def get_game_history():
    """获取游戏历史记录"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        level_id = request.args.get('level_id', type=int)
        
        query = GameHistory.query.filter_by(user_id=user_id)
        
        if level_id:
            query = query.filter_by(level_id=level_id)
        
        histories = query.order_by(GameHistory.played_at.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        histories_data = [history.to_dict() for history in histories.items]
        
        return jsonify({
            'histories': histories_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': histories.total,
                'pages': histories.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏历史失败: {str(e)}'}), 500


@levels_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_user_progress():
    """获取用户游戏进度"""
    try:
        user_id = get_jwt_identity()
        
        # 获取总关卡数
        total_levels = Level.query.filter_by(is_active=True).count()
        
        # 获取用户记录统计
        user_records = LevelRecord.query.filter_by(user_id=user_id).all()
        
        completed_levels = sum(1 for record in user_records if record.status == 'completed')
        total_stars = sum(record.stars for record in user_records)
        total_attempts = sum(record.total_attempts for record in user_records)
        total_time = sum(record.total_time_seconds for record in user_records)
        
        # 计算进度百分比
        progress_percent = round((completed_levels / total_levels * 100), 2) if total_levels > 0 else 0
        
        # 获取成就统计（这里可以根据具体需求定义成就）
        achievements = 0
        achievements_total = 30  # 假设总共30个成就
        
        # 简单的成就计算示例
        if total_stars >= 10:
            achievements += 1
        if total_stars >= 50:
            achievements += 1
        if total_stars >= 100:
            achievements += 1
        if completed_levels >= 5:
            achievements += 1
        if completed_levels >= 20:
            achievements += 1
        
        achievement_percent = round((achievements / achievements_total * 100), 2)
        
        return jsonify({
            'progress': {
                'total_levels': total_levels,
                'completed_levels': completed_levels,
                'progress_percent': progress_percent,
                'total_stars': total_stars,
                'total_attempts': total_attempts,
                'total_time_hours': round(total_time / 3600, 2),
                'achievements': achievements,
                'achievements_total': achievements_total,
                'achievement_percent': achievement_percent
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取用户进度失败: {str(e)}'}), 500


# 管理员接口

@levels_bp.route('/admin/levels', methods=['POST'])
@jwt_required()
def create_level():
    """创建关卡（管理员功能）"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'difficulty']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必填字段'}), 400
        
        level = Level(
            title=data['title'],
            description=data.get('description'),
            difficulty=data['difficulty'],
            estimated_time_minutes=data.get('estimated_time_minutes', 5),
            max_score=data.get('max_score', 1000),
            unlock_level_id=data.get('unlock_level_id'),
            unlock_stars_required=data.get('unlock_stars_required', 0),
            reward_coins=data.get('reward_coins', 100),
            reward_exp=data.get('reward_exp', 50),
            sort_order=data.get('sort_order', 0)
        )
        
        # 设置任务配置
        if 'tasks_config' in data:
            level.set_tasks_config(data['tasks_config'])
        
        db.session.add(level)
        db.session.commit()
        
        return jsonify({
            'message': '关卡创建成功',
            'level': level.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建关卡失败: {str(e)}'}), 500