"""
Gunicorn 配置文件
"""
import os
import multiprocessing

# 服务器套接字
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
backlog = 2048

# Worker 进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# 重启
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 日志
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程命名
proc_name = 'explode_word_backend'

# 安全
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL (如果需要)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# 用户和组 (生产环境建议设置)
# user = "www-data"
# group = "www-data"

# 临时目录
tmp_upload_dir = None

# 环境变量
raw_env = [
    'FLASK_ENV=production',
]