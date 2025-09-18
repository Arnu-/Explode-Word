# SQLite 数据库配置说明

## 当前配置

你的应用已经配置为使用 SQLite 数据库，这是一个轻量级的文件数据库，非常适合开发和中小型应用。

## 数据库文件位置

- **开发环境**: `backend/explode_word.db`
- **生产环境**: `backend/explode_word_prod.db`
- **测试环境**: 内存数据库 (`:memory:`)

## 初始化数据库

### 方法一：使用现有脚本
```bash
cd backend
python init_db.py
```

### 方法二：使用 Flask-Migrate
```bash
cd backend
export FLASK_APP=wsgi.py
flask db upgrade
```

### 方法三：在应用中初始化
```bash
cd backend
python -c "
from app import create_app, db
app = create_app('production')
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"
```

## 数据库备份

SQLite 数据库备份非常简单，只需要复制数据库文件：

```bash
# 备份数据库
cp explode_word_prod.db explode_word_backup_$(date +%Y%m%d_%H%M%S).db

# 恢复数据库
cp explode_word_backup_20240918_160000.db explode_word_prod.db
```

## 性能优化

对于 SQLite，可以在配置中添加以下优化：

```python
# 在 config.py 中可以添加 SQLite 特定配置
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'check_same_thread': False,
        'timeout': 20
    }
}
```

## 注意事项

1. **并发限制**: SQLite 对写操作有并发限制，但对于大多数应用足够使用
2. **文件权限**: 确保应用有读写数据库文件的权限
3. **备份策略**: 定期备份数据库文件
4. **迁移**: 如果将来需要迁移到 MySQL/PostgreSQL，Flask-Migrate 可以帮助处理