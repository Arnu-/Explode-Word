# 游戏记录系统设计文档

## 概述

本文档描述了 Explode Word 游戏的记录系统设计，包括数据结构、API接口和前端集成。

## 数据结构设计

### 1. 关卡模型 (Level)

```python
class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)          # 关卡标题
    difficulty = db.Column(db.String(20), nullable=False)      # 难度等级
    estimated_time_minutes = db.Column(db.Integer, default=5)  # 预计完成时间
    max_score = db.Column(db.Integer, default=1000)           # 最高可能分数
    tasks_config = db.Column(db.Text, nullable=True)          # 任务配置(JSON)
    unlock_level_id = db.Column(db.Integer, nullable=True)    # 解锁条件
    unlock_stars_required = db.Column(db.Integer, default=0)  # 需要星星数
    reward_coins = db.Column(db.Integer, default=100)         # 奖励金币
    is_active = db.Column(db.Boolean, default=True)           # 是否激活
```

### 2. 用户关卡记录 (LevelRecord)

```python
class LevelRecord(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    best_score = db.Column(db.Integer, default=0)             # 历史最高分
    stars = db.Column(db.Integer, default=0)                  # 星级评价(1-3)
    status = db.Column(db.String(20), default='locked')       # 关卡状态
    tasks_completion = db.Column(db.Text, nullable=True)      # 任务完成状态
    total_attempts = db.Column(db.Integer, default=0)         # 总尝试次数
    completed_attempts = db.Column(db.Integer, default=0)     # 完成次数
    last_played_at = db.Column(db.DateTime, nullable=True)    # 最后游戏时间
    best_time_seconds = db.Column(db.Integer, nullable=True)  # 最佳完成时间
```

### 3. 游戏历史记录 (GameHistory)

```python
class GameHistory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    score = db.Column(db.Integer, default=0)                  # 本次得分
    time_seconds = db.Column(db.Integer, default=0)           # 用时
    stars_earned = db.Column(db.Integer, default=0)           # 获得星级
    correct_answers = db.Column(db.Integer, default=0)        # 正确答案数
    wrong_answers = db.Column(db.Integer, default=0)          # 错误答案数
    tasks_result = db.Column(db.Text, nullable=True)          # 任务结果
    is_completed = db.Column(db.Boolean, default=False)       # 是否完成
    is_new_record = db.Column(db.Boolean, default=False)      # 是否新纪录
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## API 接口

### 关卡相关接口

#### 1. 获取关卡列表
```
GET /api/levels/
```
返回用户的所有关卡信息，包括游戏记录。

#### 2. 开始关卡
```
POST /api/levels/{level_id}/start
```
开始指定关卡，更新尝试次数和最后游戏时间。

#### 3. 完成关卡
```
POST /api/levels/{level_id}/complete
```
提交游戏结果，更新记录和解锁新关卡。

请求体：
```json
{
  "score": 12450,
  "time_seconds": 58,
  "correct_answers": 15,
  "wrong_answers": 3,
  "tasks_result": [
    {"completed": true, "value": 18},
    {"completed": false, "value": 65},
    {"completed": true, "value": 0}
  ]
}
```

#### 4. 获取游戏历史
```
GET /api/levels/history?page=1&per_page=20&level_id=1
```

#### 5. 获取用户进度
```
GET /api/levels/progress
```
返回用户的总体游戏进度统计。

## 前端集成

### 1. 服务层 (levelService.js)

```javascript
import levelService from '@/services/levelService.js'

// 获取关卡列表
const levels = await levelService.getLevels()

// 开始关卡
await levelService.startLevel(levelId)

// 完成关卡
await levelService.completeLevel(levelId, gameResult)

// 获取用户进度
const progress = await levelService.getUserProgress()
```

### 2. 组件更新

#### LevelSelect.vue
- 集成真实API数据
- 添加加载和错误状态
- 显示用户进度统计

#### LevelDetailsPanel.vue
- 显示关卡详细信息
- 展示任务完成状态
- 显示历史最高分和星级

## 星级评价算法

星级基于以下因素计算：

1. **分数权重** (0-2星)
   - 90%+ 最高分：2星
   - 70%+ 最高分：1星

2. **时间加成** (0-1星)
   - 在预计时间80%内完成：+1星

3. **任务完成** (0-1星)
   - 完成所有任务：+1星

最终星级 = min(3, 分数星级 + 时间加成 + 任务加成)

## 数据库初始化

### 1. 创建演示用户
```bash
cd backend
python scripts/create_demo_user.py
```

### 2. 初始化关卡数据
```bash
python scripts/init_levels.py
```

### 3. 一键初始化所有数据
```bash
python scripts/setup_game_data.py
```

## 前端界面展示

### 关卡卡片显示信息：
- 关卡编号和标题
- 难度等级（简单/中等/困难）
- 星级评价（0-3星）
- 关卡状态（locked/available/completed/coming-soon）

### 关卡详情面板显示：
- 关卡描述和预计时间
- 历史最高分
- 任务列表和完成状态
- 最后游戏时间

### 进度统计显示：
- 总体游戏进度（完成关卡数/总关卡数）
- 收集星星数量
- 成就进度

## 部署说明

### 后端部署
1. 运行数据库迁移：`flask db upgrade`
2. 初始化游戏数据：`python scripts/setup_game_data.py`
3. 启动后端服务

### 前端部署
1. 确保API地址配置正确（`frontend/src/config/env.js`）
2. 构建前端项目：`npm run build`
3. 部署到Web服务器

## 测试账号

- 用户名：`demo`
- 密码：`demo123`
- 包含示例游戏记录和进度数据

## 扩展功能

### 未来可扩展的功能：
1. 排行榜系统
2. 成就系统
3. 每日挑战
4. 多人竞技模式
5. 关卡编辑器
6. 数据分析和统计

## 注意事项

1. 所有API调用都需要JWT认证
2. 前端有降级机制，API失败时使用模拟数据
3. 数据库使用外键约束确保数据一致性
4. 星级计算逻辑可根据游戏平衡性调整
5. 任务配置使用JSON格式，便于扩展新任务类型