"""
用户模型
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(80), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    
    # 游戏统计
    total_games = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # 关系
    game_sessions = db.relationship('GameSession', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def win_rate(self):
        """胜率"""
        if self.total_games == 0:
            return 0
        return round(self.total_wins / self.total_games * 100, 2)
    
    @property
    def average_score(self):
        """平均分数"""
        if self.total_games == 0:
            return 0
        return round(self.total_score / self.total_games, 2)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'avatar_url': self.avatar_url,
            'total_games': self.total_games,
            'total_wins': self.total_wins,
            'best_score': self.best_score,
            'win_rate': self.win_rate,
            'average_score': self.average_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'