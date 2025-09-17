"""
应用配置文件
支持 SQLite（默认）和 MySQL 数据库配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录
basedir = Path(__file__).parent.parent.absolute()


class Config:
    """基础配置类"""
    
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'explode-word-secret-key-2024'
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-explode-word'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1小时
    
    # CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # 数据库配置
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite').lower()
    
    # SQLite 配置（默认）
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH') or str(basedir / 'explode_word.db')
    
    # MySQL 配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'explode_word')
    
    # SQLAlchemy 配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # 默认使用 SQLite 数据库
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{str(basedir / "explode_word.db")}'
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # 开发环境日志配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/explode_word.log', 
                maxBytes=10240, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Explode Word startup')


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # 生产环境日志配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/explode_word.log', 
            maxBytes=1024*1024, 
            backupCount=20
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.WARNING)


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    # 测试环境使用内存数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = 60  # 测试时短一些


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}