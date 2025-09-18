"""
基于词库的游戏API
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.game import Game, GameSession
from app.models.user import User
from app.models.vocabulary import VocabularyLibrary, WordGroup, VocabularyWord
import random
import string

vocabulary_game_bp = Blueprint('vocabulary_game', __name__)


def generate_session_code():
    """生成游戏会话代码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@vocabulary_game_bp.route('/start', methods=['POST'])
@jwt_required()
def start_vocabulary_game():
    """开始基于词库的游戏"""
    try:
        user_id = get_jwt_identity()
        # JWT identity 是字符串，需要转换为整数
        user_id = int(user_id) if user_id else None
        data = request.get_json()
        
        # 验证必填字段
        if 'library_id' not in data or 'group_id' not in data:
            return jsonify({'error': '缺少词库ID或词组ID'}), 400
        
        library_id = data['library_id']
        group_id = data['group_id']
        
        # 验证词库和词组是否存在
        library = VocabularyLibrary.query.get(library_id)
        if not library:
            return jsonify({'error': '词库不存在'}), 404
        
        group = WordGroup.query.get(group_id)
        if not group or group.library_id != library_id:
            return jsonify({'error': '词组不存在或不属于指定词库'}), 404
        
        # 获取词组中的单词
        words = VocabularyWord.query.filter_by(group_id=group_id).all()
        if not words:
            return jsonify({'error': '词组中没有单词'}), 400
        
        # 创建或获取默认游戏配置
        game = Game.query.filter_by(name='词库游戏').first()
        if not game:
            game = Game(
                name='词库游戏',
                description='基于词库的单词学习游戏',
                max_players=1,
                time_limit=300,
                word_count=len(words),
                difficulty_level=group.difficulty_level or 1
            )
            db.session.add(game)
            db.session.flush()  # 获取ID
        
        # 生成唯一的会话代码
        session_code = generate_session_code()
        while GameSession.query.filter_by(session_code=session_code).first():
            session_code = generate_session_code()
        
        # 准备单词数据
        words_data = []
        for word in words:
            words_data.append({
                'id': word.id,
                'english': word.word,
                'chinese': word.translation,
                'pronunciation': word.pronunciation,
                'difficulty_level': word.difficulty_level,
                'phonetic': word.phonetic,
                'part_of_speech': word.part_of_speech,
                'example_sentence': word.example_sentence,
                'example_translation': word.example_translation
            })
        
        # 随机打乱单词顺序
        random.shuffle(words_data)
        
        # 创建游戏会话
        session = GameSession(
            session_code=session_code,
            game_id=game.id,
            user_id=user_id,
            status='playing',
            total_rounds=1,
            started_at=datetime.utcnow()
        )
        
        # 设置单词数据
        session.set_words_data(words_data)
        
        # 设置玩家数据
        user = User.query.get(user_id)
        players_data = [{
            'user_id': user_id,
            'username': user.username,
            'nickname': user.nickname or user.username,
            'avatar_url': user.avatar_url,
            'score': 0,
            'ready': True
        }]
        session.set_players_data(players_data)
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': '游戏开始',
            'session_code': session_code,
            'session': session.to_dict(),
            'library': {
                'id': library.id,
                'name': library.name
            },
            'group': {
                'id': group.id,
                'name': group.name,
                'difficulty_level': group.difficulty_level
            },
            'words_count': len(words_data),
            'game_config': {
                'time_limit': game.time_limit,
                'word_count': len(words_data)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'开始游戏失败: {str(e)}'}), 500


@vocabulary_game_bp.route('/<session_code>/words', methods=['GET'])
@jwt_required()
def get_game_words(session_code):
    """获取游戏单词数据"""
    try:
        user_id = get_jwt_identity()
        # JWT identity 是字符串，需要转换为整数
        user_id = int(user_id) if user_id else None
        
        session = GameSession.query.filter_by(session_code=session_code).first()
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '无权访问此游戏会话'}), 403
        
        words_data = session.get_words_data()
        
        return jsonify({
            'words': words_data,
            'total_count': len(words_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取单词数据失败: {str(e)}'}), 500


@vocabulary_game_bp.route('/<session_code>/answer', methods=['POST'])
@jwt_required()
def submit_answer(session_code):
    """提交答案"""
    try:
        user_id = get_jwt_identity()
        # JWT identity 是字符串，需要转换为整数
        user_id = int(user_id) if user_id else None
        data = request.get_json()
        
        session = GameSession.query.filter_by(session_code=session_code).first()
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '无权访问此游戏会话'}), 403
        
        if session.status != 'playing':
            return jsonify({'error': '游戏未在进行中'}), 400
        
        # 验证答案数据
        if 'word_id' not in data or 'answer' not in data or 'is_correct' not in data:
            return jsonify({'error': '缺少必填字段'}), 400
        
        word_id = data['word_id']
        answer = data['answer']
        is_correct = data['is_correct']
        time_used = data.get('time_used', 0)
        
        # 更新统计数据
        if is_correct:
            session.correct_answers += 1
        else:
            session.wrong_answers += 1
        
        session.time_used += time_used
        
        # 计算分数（可以根据需要调整计分规则）
        if is_correct:
            base_score = 100
            time_bonus = max(0, 30 - time_used) * 2  # 时间奖励
            session.final_score += base_score + time_bonus
        
        db.session.commit()
        
        return jsonify({
            'message': '答案已提交',
            'is_correct': is_correct,
            'current_score': session.final_score,
            'correct_answers': session.correct_answers,
            'wrong_answers': session.wrong_answers
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交答案失败: {str(e)}'}), 500


@vocabulary_game_bp.route('/<session_code>/finish', methods=['POST'])
@jwt_required()
def finish_game(session_code):
    """结束游戏"""
    try:
        user_id = get_jwt_identity()
        # JWT identity 是字符串，需要转换为整数
        user_id = int(user_id) if user_id else None
        
        session = GameSession.query.filter_by(session_code=session_code).first()
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '无权访问此游戏会话'}), 403
        
        if session.status != 'playing':
            return jsonify({'error': '游戏未在进行中'}), 400
        
        # 更新游戏状态
        session.status = 'finished'
        session.finished_at = datetime.utcnow()
        
        # 计算最终结果
        total_questions = session.correct_answers + session.wrong_answers
        accuracy = session.accuracy
        
        # 设置游戏结果
        game_result = {
            'final_score': session.final_score,
            'correct_answers': session.correct_answers,
            'wrong_answers': session.wrong_answers,
            'total_questions': total_questions,
            'accuracy': accuracy,
            'time_used': session.time_used,
            'completed_at': session.finished_at.isoformat()
        }
        session.set_game_result(game_result)
        
        # 更新用户统计
        user = User.query.get(user_id)
        user.total_games += 1
        user.total_score += session.final_score
        
        if session.final_score > user.best_score:
            user.best_score = session.final_score
        
        if accuracy >= 80:  # 80%以上算胜利
            user.total_wins += 1
        
        db.session.commit()
        
        return jsonify({
            'message': '游戏结束',
            'result': game_result,
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'结束游戏失败: {str(e)}'}), 500


@vocabulary_game_bp.route('/<session_code>/status', methods=['GET'])
@jwt_required()
def get_game_status(session_code):
    """获取游戏状态"""
    try:
        user_id = get_jwt_identity()
        # JWT identity 是字符串，需要转换为整数
        user_id = int(user_id) if user_id else None
        
        session = GameSession.query.filter_by(session_code=session_code).first()
        if not session:
            return jsonify({'error': '游戏会话不存在'}), 404
        
        if session.user_id != user_id:
            return jsonify({'error': '无权访问此游戏会话'}), 403
        
        return jsonify({
            'session': session.to_dict(),
            'words_count': len(session.get_words_data()),
            'players': session.get_players_data()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取游戏状态失败: {str(e)}'}), 500