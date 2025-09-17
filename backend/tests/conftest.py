"""
测试配置文件
"""
import pytest
from app import create_app, db
from app.models.user import User
from app.models.game import Game
from app.models.word import Word, WordCategory


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建测试运行器"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """创建测试用户"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            nickname='测试用户'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_game(app):
    """创建测试游戏"""
    with app.app_context():
        game = Game(
            name='测试游戏',
            description='这是一个测试游戏',
            max_players=4,
            time_limit=300,
            word_count=20
        )
        db.session.add(game)
        db.session.commit()
        return game


@pytest.fixture
def test_category(app):
    """创建测试分类"""
    with app.app_context():
        category = WordCategory(
            name='测试分类',
            description='测试用的单词分类'
        )
        db.session.add(category)
        db.session.commit()
        return category


@pytest.fixture
def test_words(app, test_category):
    """创建测试单词"""
    with app.app_context():
        words = [
            Word(word='hello', translation='你好', category_id=test_category.id),
            Word(word='world', translation='世界', category_id=test_category.id),
            Word(word='test', translation='测试', category_id=test_category.id),
        ]
        
        for word in words:
            db.session.add(word)
        
        db.session.commit()
        return words