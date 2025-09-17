"""
单词模型
"""
from datetime import datetime
from app import db


class WordCategory(db.Model):
    """单词分类模型"""
    __tablename__ = 'word_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5难度等级
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    words = db.relationship('Word', backref='category', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'word_count': self.words.count()
        }
    
    def __repr__(self):
        return f'<WordCategory {self.name}>'


class Word(db.Model):
    """单词模型"""
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, index=True)
    translation = db.Column(db.String(200), nullable=False)
    pronunciation = db.Column(db.String(100), nullable=True)
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5难度等级
    frequency = db.Column(db.Integer, default=0)  # 使用频率
    
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('word_categories.id'), nullable=True)
    
    # 额外信息
    example_sentence = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)  # 标签，用逗号分隔
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def set_tags_list(self, tags_list):
        """设置标签列表"""
        if tags_list:
            self.tags = ','.join(tags_list)
        else:
            self.tags = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'word': self.word,
            'translation': self.translation,
            'pronunciation': self.pronunciation,
            'difficulty_level': self.difficulty_level,
            'frequency': self.frequency,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'example_sentence': self.example_sentence,
            'tags': self.get_tags_list(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Word {self.word}>'