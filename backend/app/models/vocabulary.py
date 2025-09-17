"""
词库管理模型
包含词库、词组、单词的三层结构
"""
from datetime import datetime
from app import db


class VocabularyLibrary(db.Model):
    """词库模型 - 最外层"""
    __tablename__ = 'vocabulary_libraries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # 标签，如：人教版,部编版等，用逗号分隔
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5难度等级
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)  # 排序字段
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    word_groups = db.relationship('WordGroup', backref='library', lazy='dynamic', cascade='all, delete-orphan')
    
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
    
    def get_total_words_count(self):
        """获取词库中总单词数"""
        total = 0
        for group in self.word_groups:
            total += group.vocabulary_words.count()
        return total
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tags': self.get_tags_list(),
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'groups_count': self.word_groups.count(),
            'total_words_count': self.get_total_words_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<VocabularyLibrary {self.name}>'


class WordGroup(db.Model):
    """词组模型 - 中间层，相当于关卡"""
    __tablename__ = 'word_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5难度等级
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)  # 排序字段
    
    # 外键
    library_id = db.Column(db.Integer, db.ForeignKey('vocabulary_libraries.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    vocabulary_words = db.relationship('VocabularyWord', backref='group', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'library_id': self.library_id,
            'library_name': self.library.name if self.library else None,
            'words_count': self.vocabulary_words.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<WordGroup {self.name}>'


class VocabularyWord(db.Model):
    """词汇单词模型 - 最小单位"""
    __tablename__ = 'vocabulary_words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, index=True)
    translation = db.Column(db.String(200), nullable=False)
    pronunciation = db.Column(db.String(100), nullable=True)
    phonetic = db.Column(db.String(100), nullable=True)  # 音标
    part_of_speech = db.Column(db.String(50), nullable=True)  # 词性
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5难度等级
    frequency = db.Column(db.Integer, default=0)  # 使用频率
    
    # 外键
    group_id = db.Column(db.Integer, db.ForeignKey('word_groups.id'), nullable=False)
    
    # 额外信息
    example_sentence = db.Column(db.Text, nullable=True)
    example_translation = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)  # 备注
    tags = db.Column(db.String(200), nullable=True)  # 标签，用逗号分隔
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)  # 排序字段
    
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
            'phonetic': self.phonetic,
            'part_of_speech': self.part_of_speech,
            'difficulty_level': self.difficulty_level,
            'frequency': self.frequency,
            'group_id': self.group_id,
            'group_name': self.group.name if self.group else None,
            'library_id': self.group.library_id if self.group else None,
            'library_name': self.group.library.name if self.group and self.group.library else None,
            'example_sentence': self.example_sentence,
            'example_translation': self.example_translation,
            'notes': self.notes,
            'tags': self.get_tags_list(),
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<VocabularyWord {self.word}>'