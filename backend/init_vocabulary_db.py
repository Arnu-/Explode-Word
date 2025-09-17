#!/usr/bin/env python3
"""
初始化词库数据库脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models.vocabulary import VocabularyLibrary, WordGroup, VocabularyWord

def init_vocabulary_database():
    """初始化词库数据库"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 开始初始化词库数据库...")
            
            # 创建所有表
            db.create_all()
            print("✅ 数据库表创建成功")
            
            # 检查是否已有数据
            if VocabularyLibrary.query.first():
                print("📝 词库数据已存在")
                choice = input("是否要重新创建示例数据？(y/N): ").lower().strip()
                if choice != 'y':
                    print("🔄 保持现有数据不变")
                    return
                else:
                    # 清空现有数据
                    print("🗑️ 清空现有数据...")
                    VocabularyWord.query.delete()
                    WordGroup.query.delete()
                    VocabularyLibrary.query.delete()
                    db.session.commit()
            
            # 创建示例数据
            create_sample_vocabulary_data()
            
            print("🎉 词库数据库初始化完成！")
            print("\n📋 数据统计:")
            print(f"   词库数量: {VocabularyLibrary.query.count()}")
            print(f"   词组数量: {WordGroup.query.count()}")
            print(f"   单词数量: {VocabularyWord.query.count()}")
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            db.session.rollback()
            raise

def create_sample_vocabulary_data():
    """创建示例词库数据"""
    print("📚 创建示例词库数据...")
    
    # 创建词库
    libraries = [
        {
            'name': '人教版小学英语',
            'description': '人教版小学英语词汇库，涵盖1-6年级所有重点词汇，按年级和主题分类整理',
            'tags': '人教版,小学,基础教育,K12',
            'difficulty_level': 1,
            'sort_order': 1
        },
        {
            'name': '大学英语四级词汇',
            'description': '大学英语四级考试必备词汇，按主题和词频分类，包含历年真题高频词汇',
            'tags': '四级,CET4,考试,大学英语',
            'difficulty_level': 3,
            'sort_order': 2
        },
        {
            'name': '商务英语核心词汇',
            'description': '商务场景核心词汇，涵盖会议、谈判、邮件、报告等各种商务情境',
            'tags': '商务英语,职场,BEC,商务沟通',
            'difficulty_level': 4,
            'sort_order': 3
        },
        {
            'name': '雅思词汇精选',
            'description': '雅思考试高频词汇，按听说读写四个技能分类，助力雅思高分',
            'tags': 'IELTS,雅思,出国留学,英语考试',
            'difficulty_level': 4,
            'sort_order': 4
        }
    ]
    
    created_libraries = []
    for lib_data in libraries:
        library = VocabularyLibrary(**lib_data)
        db.session.add(library)
        created_libraries.append(library)
    
    db.session.flush()  # 获取ID
    
    # 创建词组
    groups_data = [
        # 人教版小学英语词组
        {
            'name': '日常问候',
            'description': '日常生活中的问候用语',
            'difficulty_level': 1,
            'sort_order': 1,
            'library_id': created_libraries[0].id
        },
        {
            'name': '家庭成员',
            'description': '家庭成员称呼词汇',
            'difficulty_level': 1,
            'sort_order': 2,
            'library_id': created_libraries[0].id
        },
        {
            'name': '学校用品',
            'description': '学习用品相关词汇',
            'difficulty_level': 1,
            'sort_order': 3,
            'library_id': created_libraries[0].id
        },
        {
            'name': '颜色与数字',
            'description': '基础颜色和数字词汇',
            'difficulty_level': 1,
            'sort_order': 4,
            'library_id': created_libraries[0].id
        },
        
        # 大学英语四级词组
        {
            'name': '学术词汇',
            'description': '学术写作和阅读常用词汇',
            'difficulty_level': 3,
            'sort_order': 1,
            'library_id': created_libraries[1].id
        },
        {
            'name': '科技与创新',
            'description': '科技发展和创新相关词汇',
            'difficulty_level': 3,
            'sort_order': 2,
            'library_id': created_libraries[1].id
        },
        {
            'name': '环境保护',
            'description': '环境保护和可持续发展词汇',
            'difficulty_level': 3,
            'sort_order': 3,
            'library_id': created_libraries[1].id
        },
        
        # 商务英语词组
        {
            'name': '会议沟通',
            'description': '商务会议中的沟通用语',
            'difficulty_level': 4,
            'sort_order': 1,
            'library_id': created_libraries[2].id
        },
        {
            'name': '邮件写作',
            'description': '商务邮件写作常用词汇',
            'difficulty_level': 4,
            'sort_order': 2,
            'library_id': created_libraries[2].id
        },
        
        # 雅思词汇词组
        {
            'name': '雅思写作高频词',
            'description': '雅思写作任务中的高频词汇',
            'difficulty_level': 4,
            'sort_order': 1,
            'library_id': created_libraries[3].id
        }
    ]
    
    created_groups = []
    for group_data in groups_data:
        group = WordGroup(**group_data)
        db.session.add(group)
        created_groups.append(group)
    
    db.session.flush()  # 获取ID
    
    # 创建单词
    words_data = [
        # 日常问候
        {
            'word': 'hello',
            'translation': '你好',
            'pronunciation': 'həˈloʊ',
            'phonetic': '/həˈloʊ/',
            'part_of_speech': 'int.',
            'example_sentence': 'Hello, how are you today?',
            'example_translation': '你好，你今天好吗？',
            'notes': '最常用的问候语',
            'tags': '基础,问候,日常',
            'difficulty_level': 1,
            'group_id': created_groups[0].id
        },
        {
            'word': 'goodbye',
            'translation': '再见',
            'pronunciation': 'ɡʊdˈbaɪ',
            'phonetic': '/ɡʊdˈbaɪ/',
            'part_of_speech': 'int.',
            'example_sentence': 'Goodbye, see you tomorrow!',
            'example_translation': '再见，明天见！',
            'notes': '正式的告别用语',
            'tags': '基础,告别,日常',
            'difficulty_level': 1,
            'group_id': created_groups[0].id
        },
        {
            'word': 'good morning',
            'translation': '早上好',
            'pronunciation': 'ɡʊd ˈmɔːrnɪŋ',
            'phonetic': '/ɡʊd ˈmɔːrnɪŋ/',
            'part_of_speech': 'phrase',
            'example_sentence': 'Good morning, everyone!',
            'example_translation': '大家早上好！',
            'notes': '上午使用的问候语',
            'tags': '基础,问候,时间',
            'difficulty_level': 1,
            'group_id': created_groups[0].id
        },
        
        # 家庭成员
        {
            'word': 'father',
            'translation': '父亲',
            'pronunciation': 'ˈfɑːðər',
            'phonetic': '/ˈfɑːðər/',
            'part_of_speech': 'n.',
            'example_sentence': 'My father is a doctor.',
            'example_translation': '我父亲是一名医生。',
            'notes': '正式称呼，也可以说dad',
            'tags': '家庭,称呼,基础',
            'difficulty_level': 1,
            'group_id': created_groups[1].id
        },
        {
            'word': 'mother',
            'translation': '母亲',
            'pronunciation': 'ˈmʌðər',
            'phonetic': '/ˈmʌðər/',
            'part_of_speech': 'n.',
            'example_sentence': 'My mother cooks delicious food.',
            'example_translation': '我母亲做的菜很好吃。',
            'notes': '正式称呼，也可以说mom',
            'tags': '家庭,称呼,基础',
            'difficulty_level': 1,
            'group_id': created_groups[1].id
        },
        
        # 学术词汇
        {
            'word': 'analyze',
            'translation': '分析',
            'pronunciation': 'ˈænəlaɪz',
            'phonetic': '/ˈænəlaɪz/',
            'part_of_speech': 'v.',
            'example_sentence': 'We need to analyze the data carefully.',
            'example_translation': '我们需要仔细分析这些数据。',
            'notes': '学术写作中的高频动词',
            'tags': '学术,分析,四级',
            'difficulty_level': 3,
            'group_id': created_groups[4].id
        },
        {
            'word': 'significant',
            'translation': '重要的，显著的',
            'pronunciation': 'sɪɡˈnɪfɪkənt',
            'phonetic': '/sɪɡˈnɪfɪkənt/',
            'part_of_speech': 'adj.',
            'example_sentence': 'This is a significant discovery.',
            'example_translation': '这是一个重要的发现。',
            'notes': '表示重要性的形容词',
            'tags': '学术,重要,四级',
            'difficulty_level': 3,
            'group_id': created_groups[4].id
        },
        
        # 商务会议
        {
            'word': 'agenda',
            'translation': '议程',
            'pronunciation': 'əˈdʒendə',
            'phonetic': '/əˈdʒendə/',
            'part_of_speech': 'n.',
            'example_sentence': 'Let\'s review the meeting agenda.',
            'example_translation': '让我们回顾一下会议议程。',
            'notes': '会议必备词汇',
            'tags': '商务,会议,议程',
            'difficulty_level': 4,
            'group_id': created_groups[7].id
        },
        {
            'word': 'presentation',
            'translation': '演示，报告',
            'pronunciation': 'ˌpriːzenˈteɪʃn',
            'phonetic': '/ˌpriːzenˈteɪʃn/',
            'part_of_speech': 'n.',
            'example_sentence': 'She gave an excellent presentation.',
            'example_translation': '她做了一个出色的演示。',
            'notes': '商务场合常用',
            'tags': '商务,演示,报告',
            'difficulty_level': 4,
            'group_id': created_groups[7].id
        }
    ]
    
    for word_data in words_data:
        word = VocabularyWord(**word_data)
        db.session.add(word)
    
    db.session.commit()
    print("✅ 示例数据创建完成")

if __name__ == '__main__':
    init_vocabulary_database()