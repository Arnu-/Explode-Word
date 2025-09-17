"""
词库管理API
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from app import db
from app.models.vocabulary import VocabularyLibrary, WordGroup, VocabularyWord
from app.utils.validators import validate_required_fields

vocabulary_bp = Blueprint('vocabulary', __name__)


# ==================== 词库管理 ====================

@vocabulary_bp.route('/libraries', methods=['GET'])
@jwt_required()
def get_libraries():
    """获取词库列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        tags = request.args.get('tags', '')
        is_active = request.args.get('is_active', type=bool)
        
        query = VocabularyLibrary.query
        
        # 搜索过滤
        if search:
            query = query.filter(or_(
                VocabularyLibrary.name.contains(search),
                VocabularyLibrary.description.contains(search)
            ))
        
        # 标签过滤
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                query = query.filter(VocabularyLibrary.tags.contains(tag))
        
        # 状态过滤
        if is_active is not None:
            query = query.filter(VocabularyLibrary.is_active == is_active)
        
        # 排序
        query = query.order_by(VocabularyLibrary.sort_order.asc(), VocabularyLibrary.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        libraries = pagination.items
        
        return jsonify({
            'success': True,
            'data': {
                'libraries': [lib.to_dict() for lib in libraries],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_prev': pagination.has_prev,
                    'has_next': pagination.has_next
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/libraries', methods=['POST'])
@jwt_required()
def create_library():
    """创建词库"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'success': False, 'message': validation_error}), 400
        
        # 检查名称是否已存在
        existing = VocabularyLibrary.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'success': False, 'message': '词库名称已存在'}), 400
        
        library = VocabularyLibrary(
            name=data['name'],
            description=data.get('description'),
            difficulty_level=data.get('difficulty_level', 1),
            sort_order=data.get('sort_order', 0)
        )
        
        # 设置标签
        if data.get('tags'):
            library.set_tags_list(data['tags'])
        
        db.session.add(library)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词库创建成功',
            'data': library.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/libraries/<int:library_id>', methods=['GET'])
@jwt_required()
def get_library(library_id):
    """获取词库详情"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        return jsonify({
            'success': True,
            'data': library.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/libraries/<int:library_id>', methods=['PUT'])
@jwt_required()
def update_library(library_id):
    """更新词库"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        data = request.get_json()
        
        # 检查名称是否已存在（排除当前记录）
        if 'name' in data and data['name'] != library.name:
            existing = VocabularyLibrary.query.filter_by(name=data['name']).first()
            if existing:
                return jsonify({'success': False, 'message': '词库名称已存在'}), 400
        
        # 更新字段
        if 'name' in data:
            library.name = data['name']
        if 'description' in data:
            library.description = data['description']
        if 'difficulty_level' in data:
            library.difficulty_level = data['difficulty_level']
        if 'is_active' in data:
            library.is_active = data['is_active']
        if 'sort_order' in data:
            library.sort_order = data['sort_order']
        if 'tags' in data:
            library.set_tags_list(data['tags'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词库更新成功',
            'data': library.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/libraries/<int:library_id>', methods=['DELETE'])
@jwt_required()
def delete_library(library_id):
    """删除词库"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        
        # 检查是否有关联的词组
        if library.word_groups.count() > 0:
            return jsonify({'success': False, 'message': '词库下还有词组，无法删除'}), 400
        
        db.session.delete(library)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词库删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 词组管理 ====================

@vocabulary_bp.route('/libraries/<int:library_id>/groups', methods=['GET'])
@jwt_required()
def get_groups(library_id):
    """获取词库下的词组列表"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        is_active = request.args.get('is_active', type=bool)
        
        query = WordGroup.query.filter_by(library_id=library_id)
        
        # 搜索过滤
        if search:
            query = query.filter(or_(
                WordGroup.name.contains(search),
                WordGroup.description.contains(search)
            ))
        
        # 状态过滤
        if is_active is not None:
            query = query.filter(WordGroup.is_active == is_active)
        
        # 排序
        query = query.order_by(WordGroup.sort_order.asc(), WordGroup.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        groups = pagination.items
        
        return jsonify({
            'success': True,
            'data': {
                'library': library.to_dict(),
                'groups': [group.to_dict() for group in groups],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_prev': pagination.has_prev,
                    'has_next': pagination.has_next
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/libraries/<int:library_id>/groups', methods=['POST'])
@jwt_required()
def create_group(library_id):
    """创建词组"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'success': False, 'message': validation_error}), 400
        
        # 检查名称是否已存在（同一词库下）
        existing = WordGroup.query.filter_by(library_id=library_id, name=data['name']).first()
        if existing:
            return jsonify({'success': False, 'message': '词组名称已存在'}), 400
        
        group = WordGroup(
            name=data['name'],
            description=data.get('description'),
            difficulty_level=data.get('difficulty_level', 1),
            sort_order=data.get('sort_order', 0),
            library_id=library_id
        )
        
        db.session.add(group)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词组创建成功',
            'data': group.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/groups/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    """获取词组详情"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        return jsonify({
            'success': True,
            'data': group.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/groups/<int:group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    """更新词组"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        data = request.get_json()
        
        # 检查名称是否已存在（同一词库下，排除当前记录）
        if 'name' in data and data['name'] != group.name:
            existing = WordGroup.query.filter_by(library_id=group.library_id, name=data['name']).first()
            if existing:
                return jsonify({'success': False, 'message': '词组名称已存在'}), 400
        
        # 更新字段
        if 'name' in data:
            group.name = data['name']
        if 'description' in data:
            group.description = data['description']
        if 'difficulty_level' in data:
            group.difficulty_level = data['difficulty_level']
        if 'is_active' in data:
            group.is_active = data['is_active']
        if 'sort_order' in data:
            group.sort_order = data['sort_order']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词组更新成功',
            'data': group.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    """删除词组"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        
        # 检查是否有关联的单词
        if group.vocabulary_words.count() > 0:
            return jsonify({'success': False, 'message': '词组下还有单词，无法删除'}), 400
        
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '词组删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 单词管理 ====================

@vocabulary_bp.route('/groups/<int:group_id>/words', methods=['GET'])
@jwt_required()
def get_words(group_id):
    """获取词组下的单词列表"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search = request.args.get('search', '')
        tags = request.args.get('tags', '')
        is_active = request.args.get('is_active', type=bool)
        
        query = VocabularyWord.query.filter_by(group_id=group_id)
        
        # 搜索过滤
        if search:
            query = query.filter(or_(
                VocabularyWord.word.contains(search),
                VocabularyWord.translation.contains(search)
            ))
        
        # 标签过滤
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                query = query.filter(VocabularyWord.tags.contains(tag))
        
        # 状态过滤
        if is_active is not None:
            query = query.filter(VocabularyWord.is_active == is_active)
        
        # 排序
        query = query.order_by(VocabularyWord.sort_order.asc(), VocabularyWord.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        words = pagination.items
        
        return jsonify({
            'success': True,
            'data': {
                'group': group.to_dict(),
                'words': [word.to_dict() for word in words],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_prev': pagination.has_prev,
                    'has_next': pagination.has_next
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/groups/<int:group_id>/words', methods=['POST'])
@jwt_required()
def create_word(group_id):
    """创建单词"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['word', 'translation']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return jsonify({'success': False, 'message': validation_error}), 400
        
        # 检查单词是否已存在（同一词组下）
        existing = VocabularyWord.query.filter_by(group_id=group_id, word=data['word']).first()
        if existing:
            return jsonify({'success': False, 'message': '单词已存在'}), 400
        
        word = VocabularyWord(
            word=data['word'],
            translation=data['translation'],
            pronunciation=data.get('pronunciation'),
            phonetic=data.get('phonetic'),
            part_of_speech=data.get('part_of_speech'),
            difficulty_level=data.get('difficulty_level', 1),
            example_sentence=data.get('example_sentence'),
            example_translation=data.get('example_translation'),
            notes=data.get('notes'),
            sort_order=data.get('sort_order', 0),
            group_id=group_id
        )
        
        # 设置标签
        if data.get('tags'):
            word.set_tags_list(data['tags'])
        
        db.session.add(word)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '单词创建成功',
            'data': word.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/words/<int:word_id>', methods=['GET'])
@jwt_required()
def get_word(word_id):
    """获取单词详情"""
    try:
        word = VocabularyWord.query.get_or_404(word_id)
        return jsonify({
            'success': True,
            'data': word.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/words/<int:word_id>', methods=['PUT'])
@jwt_required()
def update_word(word_id):
    """更新单词"""
    try:
        word = VocabularyWord.query.get_or_404(word_id)
        data = request.get_json()
        
        # 检查单词是否已存在（同一词组下，排除当前记录）
        if 'word' in data and data['word'] != word.word:
            existing = VocabularyWord.query.filter_by(group_id=word.group_id, word=data['word']).first()
            if existing:
                return jsonify({'success': False, 'message': '单词已存在'}), 400
        
        # 更新字段
        if 'word' in data:
            word.word = data['word']
        if 'translation' in data:
            word.translation = data['translation']
        if 'pronunciation' in data:
            word.pronunciation = data['pronunciation']
        if 'phonetic' in data:
            word.phonetic = data['phonetic']
        if 'part_of_speech' in data:
            word.part_of_speech = data['part_of_speech']
        if 'difficulty_level' in data:
            word.difficulty_level = data['difficulty_level']
        if 'example_sentence' in data:
            word.example_sentence = data['example_sentence']
        if 'example_translation' in data:
            word.example_translation = data['example_translation']
        if 'notes' in data:
            word.notes = data['notes']
        if 'is_active' in data:
            word.is_active = data['is_active']
        if 'sort_order' in data:
            word.sort_order = data['sort_order']
        if 'tags' in data:
            word.set_tags_list(data['tags'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '单词更新成功',
            'data': word.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@vocabulary_bp.route('/words/<int:word_id>', methods=['DELETE'])
@jwt_required()
def delete_word(word_id):
    """删除单词"""
    try:
        word = VocabularyWord.query.get_or_404(word_id)
        
        db.session.delete(word)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '单词删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== 批量操作 ====================

@vocabulary_bp.route('/groups/<int:group_id>/words/batch', methods=['POST'])
@jwt_required()
def batch_create_words(group_id):
    """批量创建单词"""
    try:
        group = WordGroup.query.get_or_404(group_id)
        data = request.get_json()
        
        if not data.get('words') or not isinstance(data['words'], list):
            return jsonify({'success': False, 'message': '请提供单词列表'}), 400
        
        created_words = []
        errors = []
        
        for i, word_data in enumerate(data['words']):
            try:
                # 验证必填字段
                if not word_data.get('word') or not word_data.get('translation'):
                    errors.append(f'第{i+1}行：单词和翻译为必填项')
                    continue
                
                # 检查单词是否已存在
                existing = VocabularyWord.query.filter_by(group_id=group_id, word=word_data['word']).first()
                if existing:
                    errors.append(f'第{i+1}行：单词"{word_data["word"]}"已存在')
                    continue
                
                word = VocabularyWord(
                    word=word_data['word'],
                    translation=word_data['translation'],
                    pronunciation=word_data.get('pronunciation'),
                    phonetic=word_data.get('phonetic'),
                    part_of_speech=word_data.get('part_of_speech'),
                    difficulty_level=word_data.get('difficulty_level', 1),
                    example_sentence=word_data.get('example_sentence'),
                    example_translation=word_data.get('example_translation'),
                    notes=word_data.get('notes'),
                    sort_order=word_data.get('sort_order', 0),
                    group_id=group_id
                )
                
                # 设置标签
                if word_data.get('tags'):
                    word.set_tags_list(word_data['tags'])
                
                db.session.add(word)
                created_words.append(word)
                
            except Exception as e:
                errors.append(f'第{i+1}行：{str(e)}')
        
        if created_words:
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功创建{len(created_words)}个单词',
            'data': {
                'created_count': len(created_words),
                'error_count': len(errors),
                'errors': errors
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500