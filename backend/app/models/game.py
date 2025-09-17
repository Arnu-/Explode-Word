"""
游戏模型
"""
from datetime import datetime
from app import db
import json


class Game(db.Model):
    """游戏配置模型"""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # 游戏配置
    max_players = db.Column(db.Integer, default=4)
    time_limit = db.Column(db.Integer, default=300)  # 秒
    word_count = db.Column(db.Integer, default=20)
    difficulty_level = db.Column(db.Integer, default=1)
    
    # 游戏规则配置（JSON格式）
    rules_config = db.Column(db.Text, nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    game_sessions = db.relationship('GameSession', backref='game', lazy='dynamic')
    
    def get_rules_config(self):
        """获取规则配置"""
        if self.rules_config:
            return json.loads(self.rules_config)
        return {}
    
    def set_rules_config(self, config_dict):
        """设置规则配置"""
        self.rules_config = json.dumps(config_dict)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'max_players': self.max_players,
            'time_limit': self.time_limit,
            'word_count': self.word_count,
            'difficulty_level': self.difficulty_level,
            'rules_config': self.get_rules_config(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Game {self.name}>'


class GameSession(db.Model):
    """游戏会话模型"""
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # 外键
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 游戏状态
    status = db.Column(db.String(20), default='waiting')  # waiting, playing, finished, cancelled
    current_round = db.Column(db.Integer, default=0)
    total_rounds = db.Column(db.Integer, default=1)
    
    # 游戏数据
    words_data = db.Column(db.Text, nullable=True)  # JSON格式存储单词数据
    players_data = db.Column(db.Text, nullable=True)  # JSON格式存储玩家数据
    game_result = db.Column(db.Text, nullable=True)  # JSON格式存储游戏结果
    
    # 分数和统计
    final_score = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    time_used = db.Column(db.Integer, default=0)  # 秒
    
    # 时间戳
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_words_data(self):
        """获取单词数据"""
        if self.words_data:
            return json.loads(self.words_data)
        return []
    
    def set_words_data(self, words_list):
        """设置单词数据"""
        self.words_data = json.dumps(words_list)
    
    def get_players_data(self):
        """获取玩家数据"""
        if self.players_data:
            return json.loads(self.players_data)
        return []
    
    def set_players_data(self, players_list):
        """设置玩家数据"""
        self.players_data = json.dumps(players_list)
    
    def get_game_result(self):
        """获取游戏结果"""
        if self.game_result:
            return json.loads(self.game_result)
        return {}
    
    def set_game_result(self, result_dict):
        """设置游戏结果"""
        self.game_result = json.dumps(result_dict)
    
    @property
    def accuracy(self):
        """准确率"""
        total = self.correct_answers + self.wrong_answers
        if total == 0:
            return 0
        return round(self.correct_answers / total * 100, 2)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'session_code': self.session_code,
            'game_id': self.game_id,
            'game_name': self.game.name if self.game else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'status': self.status,
            'current_round': self.current_round,
            'total_rounds': self.total_rounds,
            'final_score': self.final_score,
            'correct_answers': self.correct_answers,
            'wrong_answers': self.wrong_answers,
            'accuracy': self.accuracy,
            'time_used': self.time_used,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<GameSession {self.session_code}>'