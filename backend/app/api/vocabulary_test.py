"""
词库管理API - 测试版本（无需认证）
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_
from app import db
from app.models.vocabulary import VocabularyLibrary, WordGroup, VocabularyWord
from app.utils.validators import validate_required_fields, validate_pagination_params, validate_difficulty_level, validate_tags

vocabulary_test_bp = Blueprint('vocabulary_test', __name__)


# ==================== 词库管理 ====================

@vocabulary_test_bp.route('/libraries', methods=['GET'])
def get_libraries():
    """获取词库列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        tags = request.args.get('tags', '').strip()
        is_active = request.args.get('is_active')
        
        # 验证分页参数
        page, per_page = validate_pagination_params(page, per_page)
        
        # 构建查询
        query = VocabularyLibrary.query
        
        # 搜索条件
        if search:
            query = query.filter(
                or_(
                    VocabularyLibrary.name.contains(search),
                    VocabularyLibrary.description.contains(search)
                )
            )
        
        # 标签筛选
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag in tag_list:
                query = query.filter(VocabularyLibrary.tags.contains(tag))
        
        # 状态筛选
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            query = query.filter(VocabularyLibrary.is_active == is_active_bool)
        
        # 排序
        query = query.order_by(VocabularyLibrary.sort_order.asc(), VocabularyLibrary.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 构建返回数据
        libraries = []
        for library in pagination.items:
            # 统计词组和单词数量
            groups_count = WordGroup.query.filter_by(library_id=library.id, is_active=True).count()
            total_words_count = db.session.query(VocabularyWord).join(WordGroup).filter(
                WordGroup.library_id == library.id,
                WordGroup.is_active == True,
                VocabularyWord.is_active == True
            ).count()
            
            library_data = {
                'id': library.id,
                'name': library.name,
                'description': library.description,
                'tags': library.tags.split(',') if library.tags else [],
                'difficulty_level': library.difficulty_level,
                'is_active': library.is_active,
                'sort_order': library.sort_order,
                'groups_count': groups_count,
                'total_words_count': total_words_count,
                'created_at': library.created_at.isoformat() if library.created_at else None,
                'updated_at': library.updated_at.isoformat() if library.updated_at else None
            }
            libraries.append(library_data)
        
        return jsonify({
            'success': True,
            'data': {
                'libraries': libraries,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取词库列表失败: {str(e)}'
        }), 500


@vocabulary_test_bp.route('/libraries/<int:library_id>', methods=['GET'])
def get_library(library_id):
    """获取词库详情"""
    try:
        library = VocabularyLibrary.query.get_or_404(library_id)
        
        # 统计词组和单词数量
        groups_count = WordGroup.query.filter_by(library_id=library.id, is_active=True).count()
        total_words_count = db.session.query(VocabularyWord).join(WordGroup).filter(
            WordGroup.library_id == library.id,
            WordGroup.is_active == True,
            VocabularyWord.is_active == True
        ).count()
        
        library_data = {
            'id': library.id,
            'name': library.name,
            'description': library.description,
            'tags': library.tags.split(',') if library.tags else [],
            'difficulty_level': library.difficulty_level,
            'is_active': library.is_active,
            'sort_order': library.sort_order,
            'groups_count': groups_count,
            'total_words_count': total_words_count,
            'created_at': library.created_at.isoformat() if library.created_at else None,
            'updated_at': library.updated_at.isoformat() if library.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'data': library_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取词库详情失败: {str(e)}'
        }), 500


@vocabulary_test_bp.route('/libraries/<int:library_id>/groups', methods=['GET'])
def get_groups(library_id):
    """获取词组列表"""
    try:
        # 验证词库是否存在
        library = VocabularyLibrary.query.get_or_404(library_id)
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        is_active = request.args.get('is_active')
        
        # 验证分页参数
        page, per_page = validate_pagination_params(page, per_page)
        
        # 构建查询
        query = WordGroup.query.filter_by(library_id=library_id)
        
        # 搜索条件
        if search:
            query = query.filter(
                or_(
                    WordGroup.name.contains(search),
                    WordGroup.description.contains(search)
                )
            )
        
        # 状态筛选
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            query = query.filter(WordGroup.is_active == is_active_bool)
        
        # 排序
        query = query.order_by(WordGroup.sort_order.asc(), WordGroup.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 构建返回数据
        groups = []
        for group in pagination.items:
            # 统计单词数量
            words_count = VocabularyWord.query.filter_by(group_id=group.id, is_active=True).count()
            
            group_data = {
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'difficulty_level': group.difficulty_level,
                'is_active': group.is_active,
                'sort_order': group.sort_order,
                'library_id': group.library_id,
                'words_count': words_count,
                'created_at': group.created_at.isoformat() if group.created_at else None,
                'updated_at': group.updated_at.isoformat() if group.updated_at else None
            }
            groups.append(group_data)
        
        return jsonify({
            'success': True,
            'data': {
                'groups': groups,
                'library': {
                    'id': library.id,
                    'name': library.name
                },
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取词组列表失败: {str(e)}'
        }), 500


@vocabulary_test_bp.route('/groups/<int:group_id>/words', methods=['GET'])
def get_words(group_id):
    """获取单词列表"""
    try:
        # 验证词组是否存在
        group = WordGroup.query.get_or_404(group_id)
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search = request.args.get('search', '').strip()
        is_active = request.args.get('is_active')
        
        # 验证分页参数
        page, per_page = validate_pagination_params(page, per_page)
        
        # 构建查询
        query = VocabularyWord.query.filter_by(group_id=group_id)
        
        # 搜索条件
        if search:
            query = query.filter(
                or_(
                    VocabularyWord.word.contains(search),
                    VocabularyWord.translation.contains(search),
                    VocabularyWord.tags.contains(search)
                )
            )
        
        # 状态筛选
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            query = query.filter(VocabularyWord.is_active == is_active_bool)
        
        # 排序
        query = query.order_by(VocabularyWord.created_at.desc())
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 构建返回数据
        words = []
        for word in pagination.items:
            word_data = {
                'id': word.id,
                'word': word.word,
                'translation': word.translation,
                'pronunciation': word.pronunciation,
                'phonetic': word.phonetic,
                'part_of_speech': word.part_of_speech,
                'example_sentence': word.example_sentence,
                'example_translation': word.example_translation,
                'notes': word.notes,
                'tags': word.tags.split(',') if word.tags else [],
                'difficulty_level': word.difficulty_level,
                'is_active': word.is_active,
                'group_id': word.group_id,
                'created_at': word.created_at.isoformat() if word.created_at else None,
                'updated_at': word.updated_at.isoformat() if word.updated_at else None
            }
            words.append(word_data)
        
        return jsonify({
            'success': True,
            'data': {
                'words': words,
                'group': {
                    'id': group.id,
                    'name': group.name,
                    'library_id': group.library_id
                },
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取单词列表失败: {str(e)}'
        }), 500