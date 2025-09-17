"""
单词相关API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.word import Word, WordCategory
import random

words_bp = Blueprint('words', __name__)


@words_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取单词分类列表"""
    try:
        categories = WordCategory.query.filter_by(is_active=True).all()
        categories_data = [category.to_dict() for category in categories]
        
        return jsonify({'categories': categories_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取分类列表失败: {str(e)}'}), 500


@words_bp.route('/random', methods=['GET'])
def get_random_words():
    """获取随机单词"""
    try:
        # 获取查询参数
        count = request.args.get('count', 20, type=int)
        category_id = request.args.get('category_id', type=int)
        difficulty_level = request.args.get('difficulty_level', type=int)
        
        # 构建查询
        query = Word.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if difficulty_level:
            query = query.filter_by(difficulty_level=difficulty_level)
        
        # 获取所有符合条件的单词
        all_words = query.all()
        
        if not all_words:
            return jsonify({'error': '没有找到符合条件的单词'}), 404
        
        # 随机选择指定数量的单词
        selected_words = random.sample(
            all_words, 
            min(count, len(all_words))
        )
        
        words_data = [word.to_dict() for word in selected_words]
        
        return jsonify({
            'words': words_data,
            'total_available': len(all_words)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取随机单词失败: {str(e)}'}), 500


@words_bp.route('/search', methods=['GET'])
def search_words():
    """搜索单词"""
    try:
        query = request.args.get('q', '').strip()
        category_id = request.args.get('category_id', type=int)
        difficulty_level = request.args.get('difficulty_level', type=int)
        limit = request.args.get('limit', 50, type=int)
        
        # 构建查询
        word_query = Word.query.filter_by(is_active=True)
        
        if query:
            word_query = word_query.filter(
                (Word.word.contains(query)) | 
                (Word.translation.contains(query))
            )
        
        if category_id:
            word_query = word_query.filter_by(category_id=category_id)
        
        if difficulty_level:
            word_query = word_query.filter_by(difficulty_level=difficulty_level)
        
        words = word_query.limit(limit).all()
        words_data = [word.to_dict() for word in words]
        
        return jsonify({'words': words_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'搜索单词失败: {str(e)}'}), 500


@words_bp.route('/', methods=['POST'])
@jwt_required()
def create_word():
    """创建单词（管理员功能）"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not all(k in data for k in ('word', 'translation')):
            return jsonify({'error': '缺少必填字段'}), 400
        
        # 检查单词是否已存在
        existing_word = Word.query.filter_by(word=data['word']).first()
        if existing_word:
            return jsonify({'error': '单词已存在'}), 400
        
        word = Word(
            word=data['word'],
            translation=data['translation'],
            pronunciation=data.get('pronunciation'),
            difficulty_level=data.get('difficulty_level', 1),
            category_id=data.get('category_id'),
            example_sentence=data.get('example_sentence')
        )
        
        # 设置标签
        if 'tags' in data:
            word.set_tags_list(data['tags'])
        
        db.session.add(word)
        db.session.commit()
        
        return jsonify({
            'message': '单词创建成功',
            'word': word.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建单词失败: {str(e)}'}), 500


@words_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """创建单词分类（管理员功能）"""
    try:
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': '缺少分类名称'}), 400
        
        # 检查分类是否已存在
        existing_category = WordCategory.query.filter_by(name=data['name']).first()
        if existing_category:
            return jsonify({'error': '分类已存在'}), 400
        
        category = WordCategory(
            name=data['name'],
            description=data.get('description'),
            difficulty_level=data.get('difficulty_level', 1)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': '分类创建成功',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建分类失败: {str(e)}'}), 500


@words_bp.route('/<int:word_id>', methods=['PUT'])
@jwt_required()
def update_word(word_id):
    """更新单词（管理员功能）"""
    try:
        word = Word.query.get(word_id)
        
        if not word:
            return jsonify({'error': '单词不存在'}), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'word' in data:
            word.word = data['word']
        if 'translation' in data:
            word.translation = data['translation']
        if 'pronunciation' in data:
            word.pronunciation = data['pronunciation']
        if 'difficulty_level' in data:
            word.difficulty_level = data['difficulty_level']
        if 'category_id' in data:
            word.category_id = data['category_id']
        if 'example_sentence' in data:
            word.example_sentence = data['example_sentence']
        if 'tags' in data:
            word.set_tags_list(data['tags'])
        if 'is_active' in data:
            word.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': '单词更新成功',
            'word': word.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新单词失败: {str(e)}'}), 500


@words_bp.route('/batch', methods=['POST'])
@jwt_required()
def batch_create_words():
    """批量创建单词（管理员功能）"""
    try:
        data = request.get_json()
        
        if 'words' not in data or not isinstance(data['words'], list):
            return jsonify({'error': '无效的数据格式'}), 400
        
        created_words = []
        errors = []
        
        for word_data in data['words']:
            try:
                # 验证必填字段
                if not all(k in word_data for k in ('word', 'translation')):
                    errors.append(f"单词 {word_data.get('word', '未知')} 缺少必填字段")
                    continue
                
                # 检查是否已存在
                existing = Word.query.filter_by(word=word_data['word']).first()
                if existing:
                    errors.append(f"单词 {word_data['word']} 已存在")
                    continue
                
                word = Word(
                    word=word_data['word'],
                    translation=word_data['translation'],
                    pronunciation=word_data.get('pronunciation'),
                    difficulty_level=word_data.get('difficulty_level', 1),
                    category_id=word_data.get('category_id'),
                    example_sentence=word_data.get('example_sentence')
                )
                
                if 'tags' in word_data:
                    word.set_tags_list(word_data['tags'])
                
                db.session.add(word)
                created_words.append(word_data['word'])
                
            except Exception as e:
                errors.append(f"创建单词 {word_data.get('word', '未知')} 失败: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': f'批量创建完成，成功创建 {len(created_words)} 个单词',
            'created_words': created_words,
            'errors': errors
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'批量创建失败: {str(e)}'}), 500