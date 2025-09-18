# 前端代理配置说明

本项目已配置 Vite 代理功能，用于在开发环境下将前端 API 请求代理到后端服务。

## 配置概览

### Vite 代理配置

在 `vite.config.js` 中配置了代理规则：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:5000',
      changeOrigin: true,
      secure: false
    }
  }
}
```

### 环境配置

在 `src/config/env.js` 中配置了不同环境的 API 地址：

- **开发环境**: `/api` (通过 Vite 代理转发到 `http://127.0.0.1:5000`)
- **生产环境**: `https://your-backend-domain.com/api` (需要替换为实际的后端域名)
- **测试环境**: `https://test-backend-domain.com/api` (需要替换为测试环境域名)

## 使用方法

### 1. 启动后端服务

确保后端服务正在运行：

```bash
cd backend
python run.py
```

默认后端服务会在 `http://127.0.0.1:5000` 启动。

### 2. 启动前端开发服务器

```bash
cd frontend
npm run dev
```

### 3. 在组件中使用 API

```javascript
import { apiClient } from '@/utils/api.js'

// 发送 GET 请求
const users = await apiClient.get('/users')

// 发送 POST 请求
const newUser = await apiClient.post('/users', {
  name: '张三',
  email: 'zhangsan@example.com'
})
```

### 4. 使用预定义的 API 方法

```javascript
import { wordApi, userApi, authApi } from '@/utils/apiExample.js'

// 获取单词列表
const words = await wordApi.getWords()

// 用户登录
const loginResult = await authApi.login({
  username: 'admin',
  password: 'password'
})
```

## 代理工作原理

1. 前端发送请求到 `/api/users`
2. Vite 开发服务器拦截该请求
3. 将请求代理转发到 `http://127.0.0.1:5000/api/users`
4. 后端处理请求并返回响应
5. Vite 将响应返回给前端

## 配置说明

### 代理选项

- `target`: 后端服务地址
- `changeOrigin`: 改变请求头中的 origin 字段
- `secure`: 是否验证 SSL 证书（开发环境设为 false）
- `rewrite`: 可选，重写请求路径

### 路径重写示例

如果后端 API 不需要 `/api` 前缀，可以使用路径重写：

```javascript
'/api': {
  target: 'http://127.0.0.1:5000',
  changeOrigin: true,
  secure: false,
  rewrite: (path) => path.replace(/^\/api/, '')
}
```

## 生产环境部署

在生产环境中，需要：

1. 更新 `src/config/env.js` 中的生产环境 API 地址
2. 确保后端服务支持 CORS（跨域资源共享）
3. 配置反向代理（如 Nginx）或使用相同域名部署前后端

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排除

### 常见问题

1. **代理不工作**
   - 检查后端服务是否启动
   - 确认后端端口是否为 5000
   - 查看浏览器开发者工具的网络面板

2. **CORS 错误**
   - 确保后端配置了正确的 CORS 设置
   - 检查 `changeOrigin: true` 是否设置

3. **请求超时**
   - 检查后端服务响应时间
   - 调整 `API_TIMEOUT` 配置

### 调试技巧

1. 在浏览器开发者工具中查看网络请求
2. 检查 Vite 开发服务器控制台输出
3. 使用 `console.log` 在 API 客户端中添加调试信息

## 相关文件

- `vite.config.js` - Vite 代理配置
- `src/config/env.js` - 环境配置
- `src/utils/api.js` - API 客户端
- `src/utils/apiExample.js` - API 使用示例