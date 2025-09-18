"""
Flask应用工厂函数
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()


def create_app(config_name='development'):
    """
    应用工厂函数
    
    Args:
        config_name (str): 配置环境名称
        
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    config_obj = config[config_name]
    app.config.from_object(config_obj)
    
    # 初始化配置（动态设置数据库URI）
    config_obj.init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    
    # 注册蓝图
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 注册错误处理器
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app