"""
添加词库管理相关表的迁移脚本
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.vocabulary import VocabularyLibrary, WordGroup, VocabularyWord

def create_vocabulary_tables():
    """创建词库管理相关表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✅ 词库管理表创建成功！")
            
            # 创建一些示例数据
            create_sample_data()
            
        except Exception as e:
            print(f"❌ 创建表失败: {e}")
            db.session.rollback()

def create_sample_data():
    """创建示例数据"""
    try:
        # 检查是否已有数据
        if VocabularyLibrary.query.first():
            print("📝 词库数据已存在，跳过示例数据创建")
            return
        
        # 创建示例词库
        library1 = VocabularyLibrary(
            name="人教版小学英语",
            description="人教版小学英语词汇库，包含1-6年级所有重点词汇",
            tags="人教版,小学,基础",
            difficulty_level=1,
            sort_order=1
        )
        
        library2 = VocabularyLibrary(
            name="大学英语四级词汇",
            description="大学英语四级考试必备词汇，按主题分类整理",
            tags="四级,考试,大学",
            difficulty_level=3,
            sort_order=2
        )
        
        db.session.add(library1)
        db.session.add(library2)
        db.session.flush()  # 获取ID
        
        # 创建示例词组
        group1 = WordGroup(
            name="日常用语",
            description="日常生活中常用的英语表达",
            difficulty_level=1,
            sort_order=1,
            library_id=library1.id
        )
        
        group2 = WordGroup(
            name="学校生活",
            description="与学校生活相关的词汇",
            difficulty_level=1,
            sort_order=2,
            library_id=library1.id
        )
        
        group3 = WordGroup(
            name="商务英语",
            description="商务场景常用词汇",
            difficulty_level=3,
            sort_order=1,
            library_id=library2.id
        )
        
        db.session.add(group1)
        db.session.add(group2)
        db.session.add(group3)
        db.session.flush()  # 获取ID
        
        # 创建示例单词
        words_data = [
            # 日常用语
            {
                'word': 'hello',
                'translation': '你好',
                'pronunciation': 'həˈloʊ',
                'phonetic': '/həˈloʊ/',
                'part_of_speech': 'int.',
                'example_sentence': 'Hello, how are you?',
                'example_translation': '你好，你好吗？',
                'tags': '基础,问候',
                'group_id': group1.id
            },
            {
                'word': 'goodbye',
                'translation': '再见',
                'pronunciation': 'ɡʊdˈbaɪ',
                'phonetic': '/ɡʊdˈbaɪ/',
                'part_of_speech': 'int.',
                'example_sentence': 'Goodbye, see you tomorrow.',
                'example_translation': '再见，明天见。',
                'tags': '基础,告别',
                'group_id': group1.id
            },
            {
                'word': 'thank you',
                'translation': '谢谢',
                'pronunciation': 'θæŋk juː',
                'phonetic': '/θæŋk juː/',
                'part_of_speech': 'phrase',
                'example_sentence': 'Thank you for your help.',
                'example_translation': '谢谢你的帮助。',
                'tags': '基础,礼貌',
                'group_id': group1.id
            },
            # 学校生活
            {
                'word': 'school',
                'translation': '学校',
                'pronunciation': 'skuːl',
                'phonetic': '/skuːl/',
                'part_of_speech': 'n.',
                'example_sentence': 'I go to school every day.',
                'example_translation': '我每天都去学校。',
                'tags': '基础,教育',
                'group_id': group2.id
            },
            {
                'word': 'teacher',
                'translation': '老师',
                'pronunciation': 'ˈtiːtʃər',
                'phonetic': '/ˈtiːtʃər/',
                'part_of_speech': 'n.',
                'example_sentence': 'My teacher is very kind.',
                'example_translation': '我的老师很和蔼。',
                'tags': '基础,职业',
                'group_id': group2.id
            },
            # 商务英语
            {
                'word': 'business',
                'translation': '商业，生意',
                'pronunciation': 'ˈbɪznəs',
                'phonetic': '/ˈbɪznəs/',
                'part_of_speech': 'n.',
                'example_sentence': 'He runs a successful business.',
                'example_translation': '他经营着一家成功的企业。',
                'tags': '商务,重点',
                'group_id': group3.id
            },
            {
                'word': 'meeting',
                'translation': '会议',
                'pronunciation': 'ˈmiːtɪŋ',
                'phonetic': '/ˈmiːtɪŋ/',
                'part_of_speech': 'n.',
                'example_sentence': 'We have a meeting at 3 PM.',
                'example_translation': '我们下午3点有个会议。',
                'tags': '商务,办公',
                'group_id': group3.id
            }
        ]
        
        for word_data in words_data:
            word = VocabularyWord(
                word=word_data['word'],
                translation=word_data['translation'],
                pronunciation=word_data.get('pronunciation'),
                phonetic=word_data.get('phonetic'),
                part_of_speech=word_data.get('part_of_speech'),
                example_sentence=word_data.get('example_sentence'),
                example_translation=word_data.get('example_translation'),
                tags=word_data.get('tags'),
                difficulty_level=1,
                group_id=word_data['group_id']
            )
            db.session.add(word)
        
        db.session.commit()
        print("✅ 示例数据创建成功！")
        print(f"📊 创建了 {len([library1, library2])} 个词库")
        print(f"📊 创建了 {len([group1, group2, group3])} 个词组")
        print(f"📊 创建了 {len(words_data)} 个单词")
        
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        db.session.rollback()

if __name__ == '__main__':
    create_vocabulary_tables()