"""
关卡和游戏记录模型
"""
from datetime import datetime
from app import db
import json


class Level(db.Model):
    """关卡模型"""
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # 关卡配置
    difficulty = db.Column(db.String(20), nullable=False)  # 简单、中等、困难
    estimated_time_minutes = db.Column(db.Integer, default=5)  # 预计完成时间（分钟）
    max_score = db.Column(db.Integer, default=1000)  # 最高可能分数
    
    # 关卡任务（JSON格式存储）
    tasks_config = db.Column(db.Text, nullable=True)
    
    # 解锁条件
    unlock_level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=True)  # 需要完成的前置关卡
    unlock_stars_required = db.Column(db.Integer, default=0)  # 需要的星星数量
    
    # 奖励配置
    reward_coins = db.Column(db.Integer, default=100)
    reward_exp = db.Column(db.Integer, default=50)
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)  # 排序
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    level_records = db.relationship('LevelRecord', backref='level', lazy='dynamic')
    unlock_parent = db.relationship('Level', remote_side=[id], backref='unlock_children')
    
    def get_tasks_config(self):
        """获取任务配置"""
        if self.tasks_config:
            return json.loads(self.tasks_config)
        return []
    
    def set_tasks_config(self, tasks_list):
        """设置任务配置"""
        self.tasks_config = json.dumps(tasks_list)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'estimated_time_minutes': self.estimated_time_minutes,
            'max_score': self.max_score,
            'tasks_config': self.get_tasks_config(),
            'unlock_level_id': self.unlock_level_id,
            'unlock_stars_required': self.unlock_stars_required,
            'reward_coins': self.reward_coins,
            'reward_exp': self.reward_exp,
            'is_active': self.is_active,
            'sort_order': self.sort_order
        }
    
    def __repr__(self):
        return f'<Level {self.title}>'


class LevelRecord(db.Model):
    """用户关卡记录模型"""
    __tablename__ = 'level_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    
    # 游戏记录
    best_score = db.Column(db.Integer, default=0)  # 历史最高分
    total_attempts = db.Column(db.Integer, default=0)  # 总尝试次数
    completed_attempts = db.Column(db.Integer, default=0)  # 完成次数
    
    # 星级评价（1-3星）
    stars = db.Column(db.Integer, default=0)
    
    # 任务完成状态（JSON格式）
    tasks_completion = db.Column(db.Text, nullable=True)
    
    # 关卡状态
    status = db.Column(db.String(20), default='locked')  # locked, available, completed
    
    # 时间记录
    best_time_seconds = db.Column(db.Integer, nullable=True)  # 最佳完成时间（秒）
    total_time_seconds = db.Column(db.Integer, default=0)  # 总游戏时间
    last_played_at = db.Column(db.DateTime, nullable=True)  # 最后游戏时间
    first_completed_at = db.Column(db.DateTime, nullable=True)  # 首次完成时间
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 唯一约束
    __table_args__ = (db.UniqueConstraint('user_id', 'level_id', name='unique_user_level'),)
    
    def get_tasks_completion(self):
        """获取任务完成状态"""
        if self.tasks_completion:
            return json.loads(self.tasks_completion)
        return []
    
    def set_tasks_completion(self, tasks_list):
        """设置任务完成状态"""
        self.tasks_completion = json.dumps(tasks_list)
    
    @property
    def completion_rate(self):
        """完成率"""
        if self.total_attempts == 0:
            return 0
        return round(self.completed_attempts / self.total_attempts * 100, 2)
    
    @property
    def last_played_ago(self):
        """最后游戏时间描述"""
        if not self.last_played_at:
            return '—'
        
        now = datetime.utcnow()
        diff = now - self.last_played_at
        
        if diff.days > 0:
            return f'{diff.days}天前'
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f'{hours}小时前'
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f'{minutes}分钟前'
        else:
            return '刚刚'
    
    def calculate_stars(self, score, time_seconds, tasks_completed):
        """根据分数、时间和任务完成情况计算星级"""
        stars = 0
        
        # 基于分数的星级（占主要权重）
        if score >= self.level.max_score * 0.9:
            stars += 2
        elif score >= self.level.max_score * 0.7:
            stars += 1
        
        # 基于时间的星级加成
        expected_time = self.level.estimated_time_minutes * 60
        if time_seconds <= expected_time * 0.8:
            stars += 1
        
        # 基于任务完成的星级加成
        if tasks_completed >= len(self.level.get_tasks_config()):
            stars += 1
        
        # 最多3星
        return min(3, stars)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'level_id': self.level_id,
            'level_title': self.level.title if self.level else None,
            'best_score': self.best_score,
            'total_attempts': self.total_attempts,
            'completed_attempts': self.completed_attempts,
            'completion_rate': self.completion_rate,
            'stars': self.stars,
            'tasks_completion': self.get_tasks_completion(),
            'status': self.status,
            'best_time_seconds': self.best_time_seconds,
            'total_time_seconds': self.total_time_seconds,
            'last_played_at': self.last_played_at.isoformat() if self.last_played_at else None,
            'last_played_ago': self.last_played_ago,
            'first_completed_at': self.first_completed_at.isoformat() if self.first_completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<LevelRecord User:{self.user_id} Level:{self.level_id}>'


class GameHistory(db.Model):
    """游戏历史记录模型"""
    __tablename__ = 'game_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('game_sessions.id'), nullable=True)
    
    # 游戏结果
    score = db.Column(db.Integer, default=0)
    time_seconds = db.Column(db.Integer, default=0)
    stars_earned = db.Column(db.Integer, default=0)
    
    # 详细统计
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    
    # 任务完成情况（JSON格式）
    tasks_result = db.Column(db.Text, nullable=True)
    
    # 游戏状态
    is_completed = db.Column(db.Boolean, default=False)
    is_new_record = db.Column(db.Boolean, default=False)  # 是否创造新纪录
    
    # 时间戳
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_tasks_result(self):
        """获取任务结果"""
        if self.tasks_result:
            return json.loads(self.tasks_result)
        return []
    
    def set_tasks_result(self, tasks_list):
        """设置任务结果"""
        self.tasks_result = json.dumps(tasks_list)
    
    @property
    def accuracy(self):
        """准确率"""
        if self.total_questions == 0:
            return 0
        return round(self.correct_answers / self.total_questions * 100, 2)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'level_id': self.level_id,
            'level_title': self.level.title if self.level else None,
            'session_id': self.session_id,
            'score': self.score,
            'time_seconds': self.time_seconds,
            'stars_earned': self.stars_earned,
            'correct_answers': self.correct_answers,
            'wrong_answers': self.wrong_answers,
            'total_questions': self.total_questions,
            'accuracy': self.accuracy,
            'tasks_result': self.get_tasks_result(),
            'is_completed': self.is_completed,
            'is_new_record': self.is_new_record,
            'played_at': self.played_at.isoformat() if self.played_at else None
        }
    
    def __repr__(self):
        return f'<GameHistory User:{self.user_id} Level:{self.level_id} Score:{self.score}>'