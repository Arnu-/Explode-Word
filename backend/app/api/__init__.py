"""
API蓝图模块
"""
from flask import Blueprint

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# 导入所有路由
from . import auth, users, games, words, game_sessions, vocabulary, vocabulary_test, levels

# 注册子蓝图
from .auth import auth_bp
from .users import users_bp
from .games import games_bp
from .words import words_bp
from .game_sessions import game_sessions_bp
from .vocabulary import vocabulary_bp
from .vocabulary_test import vocabulary_test_bp
from .levels import levels_bp

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(games_bp, url_prefix='/games')
api_bp.register_blueprint(words_bp, url_prefix='/words')
api_bp.register_blueprint(game_sessions_bp, url_prefix='/sessions')
api_bp.register_blueprint(vocabulary_bp, url_prefix='/vocabulary')
api_bp.register_blueprint(vocabulary_test_bp, url_prefix='/vocabulary-test')
api_bp.register_blueprint(levels_bp, url_prefix='/levels')