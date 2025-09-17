"""
数据验证工具
"""
import re
from flask import request


def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """验证密码强度"""
    if len(password) < 6:
        return False
    return True


def validate_username(username):
    """验证用户名格式"""
    if len(username) < 3 or len(username) > 20:
        return False
    
    # 只允许字母、数字、下划线
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def validate_session_code(session_code):
    """验证会话代码格式"""
    if len(session_code) != 8:
        return False
    
    # 只允许大写字母和数字
    pattern = r'^[A-Z0-9]+$'
    return re.match(pattern, session_code) is not None


def validate_required_fields(data, required_fields):
    """验证必填字段"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            missing_fields.append(field)
    
    if missing_fields:
        return f"缺少必填字段: {', '.join(missing_fields)}"
    return None


def validate_pagination_params(page=None, per_page=None):
    """验证分页参数"""
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 10
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:
            per_page = 100
            
        return page, per_page
    except (ValueError, TypeError):
        return 1, 10


def validate_difficulty_level(level):
    """验证难度等级"""
    try:
        level = int(level)
        if 1 <= level <= 5:
            return True, level
        return False, "难度等级必须在1-5之间"
    except (ValueError, TypeError):
        return False, "难度等级必须是数字"


def validate_tags(tags_str):
    """验证和清理标签字符串"""
    if not tags_str:
        return []
    
    # 分割标签，支持逗号和分号分隔
    tags = re.split(r'[,;，；]', tags_str)
    # 清理空白字符并过滤空标签
    cleaned_tags = [tag.strip() for tag in tags if tag.strip()]
    # 去重并限制数量
    unique_tags = list(dict.fromkeys(cleaned_tags))[:10]  # 最多10个标签
    
    return unique_tags


def validate_word_format(word):
    """验证单词格式"""
    if not word or not word.strip():
        return False, "单词不能为空"
    
    word = word.strip()
    if len(word) > 100:
        return False, "单词长度不能超过100个字符"
    
    # 允许字母、数字、空格、连字符、撇号
    if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', word):
        return False, "单词格式不正确"
    
    return True, word


def validate_translation_format(translation):
    """验证翻译格式"""
    if not translation or not translation.strip():
        return False, "翻译不能为空"
    
    translation = translation.strip()
    if len(translation) > 500:
        return False, "翻译长度不能超过500个字符"
    
    return True, translation