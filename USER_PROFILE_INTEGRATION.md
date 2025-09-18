# 用户档案真实数据集成

## 概述

本次更新将用户档案页面与后端真实数据进行了完整集成，用户现在可以查看真实的游戏战绩、统计信息和成就数据。

## 新增功能

### 后端接口

1. **用户档案接口** (`GET /api/users/profile`)
   - 获取用户完整档案信息
   - 包含用户基本信息、游戏历史、成就和统计数据
   - 自动计算用户等级、金币、星星数等

2. **更新档案接口** (`PUT /api/users/profile`)
   - 允许用户更新用户名、邮箱、昵称等信息
   - 包含重复性验证

3. **增强的统计计算**
   - 连胜天数计算
   - 平均准确率计算
   - 游戏时长格式化
   - 成就解锁逻辑

### 前端改进

1. **用户服务** (`frontend/src/services/userService.js`)
   - 封装所有用户相关的API调用
   - 数据格式化和错误处理
   - 默认数据提供

2. **认证工具** (`frontend/src/utils/auth.js`)
   - 完整的认证状态管理
   - 自动token刷新
   - 认证错误处理

3. **用户档案页面更新**
   - 真实数据加载和显示
   - 加载状态和错误处理
   - 响应式设计保持

## 数据映射

### 用户信息
- `level`: 根据游戏次数计算 (每5局升1级)
- `coins`: 使用总分作为金币
- `completedLevels`: 已完成的不同关卡数
- `totalStars`: 根据准确率计算星星数
- `accuracy`: 所有游戏的平均准确率
- `streak`: 连续游戏天数

### 游戏历史
- 显示最近20条游戏记录
- 根据准确率自动判断游戏结果和星星数
- 实时计算游戏模式（基于分数）

### 成就系统
- 6个不同类型的成就
- 基于真实游戏数据自动解锁
- 包含进度追踪

## 使用方法

### 启动后端服务

```bash
cd backend
python run.py
```

### 启动前端服务

```bash
cd frontend
npm run dev
```

### 测试API

```bash
cd backend
python test_user_profile_api.py
```

## API端点

### 用户档案相关

- `GET /api/users/profile` - 获取用户完整档案
- `PUT /api/users/profile` - 更新用户档案
- `GET /api/users/stats` - 获取用户统计信息
- `GET /api/users/leaderboard` - 获取排行榜
- `GET /api/users/search` - 搜索用户

### 认证相关

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户信息

## 数据结构

### 用户档案响应

```json
{
  "user_info": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "level": 42,
    "coins": 3250,
    "completedLevels": 28,
    "totalStars": 156,
    "totalPlayTime": "24h 30m",
    "accuracy": "89.5%",
    "streak": 7
  },
  "game_history": [
    {
      "id": 1,
      "levelId": 1,
      "levelName": "第1关：小试牛刀",
      "mode": "挑战模式",
      "score": 450,
      "duration": 180,
      "accuracy": 92,
      "result": "success",
      "stars": 3,
      "playedAt": "2024-01-15T10:30:00Z"
    }
  ],
  "achievements": [
    {
      "id": 1,
      "name": "初出茅庐",
      "description": "完成第一个关卡",
      "icon": "fa-solid fa-star",
      "unlocked": true
    }
  ],
  "statistics": {
    "weekly_games": 5,
    "average_score": 420,
    "total_time_played": 1800,
    "total_correct_answers": 150,
    "total_wrong_answers": 25
  }
}
```

## 错误处理

### 前端错误处理
- 网络错误自动重试
- 认证失效自动跳转登录
- 友好的错误提示信息
- 降级到默认数据

### 后端错误处理
- 参数验证
- 数据库错误处理
- 认证和授权检查
- 详细的错误信息返回

## 性能优化

1. **数据缓存**: 前端缓存用户数据，减少API调用
2. **懒加载**: 按需加载游戏历史记录
3. **分页支持**: 大量数据分页显示
4. **并行请求**: 同时获取多个数据源

## 安全考虑

1. **JWT认证**: 所有用户相关接口需要认证
2. **数据验证**: 前后端双重数据验证
3. **权限控制**: 用户只能访问自己的数据
4. **敏感信息保护**: 不暴露密码等敏感信息

## 未来扩展

1. **头像上传**: 支持用户自定义头像
2. **社交功能**: 好友系统和排行榜
3. **更多成就**: 扩展成就系统
4. **数据导出**: 支持游戏数据导出
5. **个性化设置**: 主题、语言等个性化选项

## 故障排除

### 常见问题

1. **认证失败**: 检查token是否有效
2. **数据加载失败**: 检查后端服务是否运行
3. **更新失败**: 检查网络连接和权限

### 调试方法

1. 查看浏览器控制台错误信息
2. 检查网络请求状态
3. 使用测试脚本验证API
4. 查看后端日志

## 贡献指南

1. 遵循现有代码风格
2. 添加适当的错误处理
3. 编写测试用例
4. 更新文档

---

**注意**: 此功能需要用户先登录才能使用。如果遇到问题，请检查认证状态和网络连接。