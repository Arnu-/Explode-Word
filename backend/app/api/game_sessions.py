"""
游戏会话相关API
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.game import Game, GameSession
from app.models.user import User
from app.models.word import Word
import random
import string

game_sessions_bp = Blueprint('game_sessions', __name__)


def generate_session_code():
    """生成游戏会话代码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@game_sessions_bp.route('/create', methods=['POST'])
@jwt_required()
def create_session():
    """创建游戏会话"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'game_id' not in data:
            return jsonify({'error': '缺少游戏ID'}), 400
        
        game = Game.query.get(data['game_id'])
        if not game or not game.is_active:
            return jsonify({'error': '游戏不存在或已停用'}), 404
        
        # 生成唯一的会话代码
        session_code = generate_session_code()
        while GameSession.query.filter_by(session_code=session_code).first():
            session_code = generate_session_code()
        
        # 创建游戏会话
        session = GameSession(
            session_code=session_code,
            game_id=game.id,
            user_id=user_id,
            total_rounds=data.get('total_rounds', 1)
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': '游戏会话创建成功',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建游戏会话失败: {str(e)}'}), 500


@game_sessions_bp.route('/<session_code>/join', methods=['POST'])
@jwt_required()
def join_session(session_code):
    """加入游戏会话"""
    try:
        user_id = get_jwt_identity()
        session = GameSession.query.filter_by(session_code=session_code).first()
        
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.status != 'waiting':
            return jsonify({'error': '游戏已开始或已结束'}), 400
        
        # 检查是否已加入
        players_data = session.get_players_data()
        if any(player['user_id'] == user_id for player in players_data):
            return jsonify({'error': '您已在游戏中'}), 400
        
        # 检查人数限制
        if len(players_data) >= session.game.max_players:
            return jsonify({'error': '游戏人数已满'}), 400
        
        # 添加玩家
        user = User.query.get(user_id)
        players_data.append({
            'user_id': user_id,
            'username': user.username,
            'nickname': user.nickname,
            'avatar_url': user.avatar_url,
            'score': 0,
            'ready': False
        })
        
        session.set_players_data(players_data)
        db.session.commit()
        
        return jsonify({
            'message': '加入游戏成功',
            'session': session.to_dict(),
            'players': players_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'加入游戏失败: {str(e)}'}), 500


@game_sessions_bp.route('/<session_code>/start', methods=['POST'])
@jwt_required()
def start_session(session_code):
    """开始游戏"""
    try:
        user_id = get_jwt_identity()
        session = GameSession.query.filter_by(session_code=session_code).first()
        
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '只有房主可以开始游戏'}), 403
        
        if session.status != 'waiting':
            return jsonify({'error': '游戏状态不正确'}), 400
        
        # 获取游戏单词
        words = Word.query.filter_by(is_active=True).all()
        if len(words) < session.game.word_count:
            return jsonify({'error': '可用单词数量不足'}), 400
        
        # 随机选择单词
        selected_words = random.sample(words, session.game.word_count)
        words_data = [word.to_dict() for word in selected_words]
        
        # 更新会话状态
        session.status = 'playing'
        session.started_at = datetime.utcnow()
        session.current_round = 1
        session.set_words_data(words_data)
        
        db.session.commit()
        
        return jsonify({
            'message': '游戏开始',
            'session': session.to_dict(),
            'words': words_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'开始游戏失败: {str(e)}'}), 500


@game_sessions_bp.route('/<session_code>/answer', methods=['POST'])
@jwt_required()
def submit_answer(session_code):
    """提交答案"""
    try:
        user_id = get_jwt_identity()
        session = GameSession.query.filter_by(session_code=session_code).first()
        
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.status != 'playing':
            return jsonify({'error': '游戏未在进行中'}), 400
        
        data = request.get_json()
        if not all(k in data for k in ('word_id', 'answer')):
            return jsonify({'error': '缺少必填字段'}), 400
        
        word_id = data['word_id']
        answer = data['answer'].strip()
        
        # 验证答案
        words_data = session.get_words_data()
        target_word = None
        for word in words_data:
            if word['id'] == word_id:
                target_word = word
                break
        
        if not target_word:
            return jsonify({'error': '单词不存在'}), 404
        
        # 检查答案是否正确
        is_correct = answer.lower() == target_word['translation'].lower()
        
        # 更新统计
        if is_correct:
            session.correct_answers += 1
            score = 10  # 基础分数
        else:
            session.wrong_answers += 1
            score = 0
        
        session.final_score += score
        
        # 更新玩家数据
        players_data = session.get_players_data()
        for player in players_data:
            if player['user_id'] == user_id:
                player['score'] += score
                break
        
        session.set_players_data(players_data)
        db.session.commit()
        
        return jsonify({
            'is_correct': is_correct,
            'score': score,
            'correct_answer': target_word['translation'],
            'total_score': session.final_score
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交答案失败: {str(e)}'}), 500


@game_sessions_bp.route('/<session_code>/finish', methods=['POST'])
@jwt_required()
def finish_session(session_code):
    """结束游戏"""
    try:
        user_id = get_jwt_identity()
        session = GameSession.query.filter_by(session_code=session_code).first()
        
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '只有房主可以结束游戏'}), 403
        
        if session.status != 'playing':
            return jsonify({'error': '游戏未在进行中'}), 400
        
        # 更新会话状态
        session.status = 'finished'
        session.finished_at = datetime.utcnow()
        
        if session.started_at:
            session.time_used = int((session.finished_at - session.started_at).total_seconds())
        
        # 更新用户统计
        user = User.query.get(user_id)
        user.total_games += 1
        user.total_score += session.final_score
        
        if session.final_score > user.best_score:
            user.best_score = session.final_score
        
        # 判断是否获胜（这里简单以分数判断，可以根据具体规则调整）
        if session.correct_answers > session.wrong_answers:
            user.total_wins += 1
        
        # 设置游戏结果
        game_result = {
            'final_score': session.final_score,
            'correct_answers': session.correct_answers,
            'wrong_answers': session.wrong_answers,
            'accuracy': session.accuracy,
            'time_used': session.time_used,
            'players': session.get_players_data()
        }
        session.set_game_result(game_result)
        
        db.session.commit()
        
        return jsonify({
            'message': '游戏结束',
            'result': game_result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'结束游戏失败: {str(e)}'}), 500


@game_sessions_bp.route('/<session_code>', methods=['GET'])
def get_session(session_code):
    """获取游戏会话信息"""
    try:
        session = GameSession.query.filter_by(session_code=session_code).first()
        
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        session_data = session.to_dict()
        session_data['players'] = session.get_players_data()
        
        # 如果游戏正在进行，返回当前单词
        if session.status == 'playing':
            session_data['words'] = session.get_words_data()
        
        return jsonify({'session': session_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏会话失败: {str(e)}'}), 500


@game_sessions_bp.route('/my-sessions', methods=['GET'])
@jwt_required()
def get_my_sessions():
    """获取我的游戏会话列表"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        sessions = GameSession.query.filter_by(user_id=user_id).order_by(
            GameSession.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        sessions_data = [session.to_dict() for session in sessions.items]
        
        return jsonify({
            'sessions': sessions_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': sessions.total,
                'pages': sessions.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏会话列表失败: {str(e)}'}), 500