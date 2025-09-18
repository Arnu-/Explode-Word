# 词库管理系统

## 系统概述

词库管理系统是一个三层级的词汇管理平台，支持词库、词组、单词的层次化管理，并提供标签分类功能。

### 系统架构

```
词库 (VocabularyLibrary)
├── 词组 (WordGroup)
│   ├── 单词 (VocabularyWord)
│   ├── 单词 (VocabularyWord)
│   └── ...
├── 词组 (WordGroup)
│   └── ...
└── ...
```

## 功能特性

### 1. 三层级管理结构
- **词库 (Library)**: 最外层的选择范围，如"人教版小学英语"、"大学英语四级词汇"
- **词组 (Group)**: 一个关卡，如"日常问候"、"家庭成员"
- **单词 (Word)**: 可用的最小单位，包含完整的词汇信息

### 2. 标签系统
- 支持多标签分类：人教版、部编版、四级、商务英语等
- 标签可用于筛选和搜索
- 支持标签的层次化管理

### 3. 完整的词汇信息
每个单词包含：
- 单词本体
- 中文翻译
- 音标和发音
- 词性
- 例句和翻译
- 难度等级
- 标签分类
- 备注信息

## 数据库设计

### 词库表 (vocabulary_libraries)
```sql
CREATE TABLE vocabulary_libraries (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,           -- 词库名称
    description TEXT,                     -- 描述
    tags VARCHAR(500),                    -- 标签（逗号分隔）
    difficulty_level INTEGER DEFAULT 1,   -- 难度等级 1-5
    is_active BOOLEAN DEFAULT TRUE,       -- 是否启用
    sort_order INTEGER DEFAULT 0,         -- 排序
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 词组表 (word_groups)
```sql
CREATE TABLE word_groups (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,           -- 词组名称
    description TEXT,                     -- 描述
    difficulty_level INTEGER DEFAULT 1,   -- 难度等级
    sort_order INTEGER DEFAULT 0,         -- 排序
    is_active BOOLEAN DEFAULT TRUE,       -- 是否启用
    library_id INTEGER NOT NULL,          -- 所属词库ID
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (library_id) REFERENCES vocabulary_libraries (id)
);
```

### 单词表 (vocabulary_words)
```sql
CREATE TABLE vocabulary_words (
    id INTEGER PRIMARY KEY,
    word VARCHAR(100) NOT NULL,           -- 单词
    translation VARCHAR(500) NOT NULL,    -- 翻译
    pronunciation VARCHAR(200),           -- 发音
    phonetic VARCHAR(200),               -- 音标
    part_of_speech VARCHAR(50),          -- 词性
    example_sentence TEXT,               -- 例句
    example_translation TEXT,            -- 例句翻译
    notes TEXT,                          -- 备注
    tags VARCHAR(500),                   -- 标签
    difficulty_level INTEGER DEFAULT 1,  -- 难度等级
    is_active BOOLEAN DEFAULT TRUE,      -- 是否启用
    group_id INTEGER NOT NULL,           -- 所属词组ID
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES word_groups (id)
);
```

## API接口

### 词库管理

#### 获取词库列表
```http
GET /api/vocabulary/libraries
```

参数：
- `page`: 页码（默认1）
- `per_page`: 每页数量（默认10）
- `search`: 搜索关键词
- `tags`: 标签筛选
- `is_active`: 状态筛选

#### 获取词库详情
```http
GET /api/vocabulary/libraries/{id}
```

#### 创建词库
```http
POST /api/vocabulary/libraries
```

请求体：
```json
{
    "name": "词库名称",
    "description": "词库描述",
    "tags": "标签1,标签2",
    "difficulty_level": 1
}
```

#### 更新词库
```http
PUT /api/vocabulary/libraries/{id}
```

#### 删除词库
```http
DELETE /api/vocabulary/libraries/{id}
```

### 词组管理

#### 获取词组列表
```http
GET /api/vocabulary/libraries/{library_id}/groups
```

#### 获取词组详情
```http
GET /api/vocabulary/groups/{id}
```

#### 创建词组
```http
POST /api/vocabulary/libraries/{library_id}/groups
```

#### 更新词组
```http
PUT /api/vocabulary/groups/{id}
```

#### 删除词组
```http
DELETE /api/vocabulary/groups/{id}
```

### 单词管理

#### 获取单词列表
```http
GET /api/vocabulary/groups/{group_id}/words
```

#### 获取单词详情
```http
GET /api/vocabulary/words/{id}
```

#### 创建单词
```http
POST /api/vocabulary/groups/{group_id}/words
```

请求体：
```json
{
    "word": "hello",
    "translation": "你好",
    "pronunciation": "həˈloʊ",
    "phonetic": "/həˈloʊ/",
    "part_of_speech": "int.",
    "example_sentence": "Hello, how are you?",
    "example_translation": "你好，你好吗？",
    "notes": "常用问候语",
    "tags": "基础,问候",
    "difficulty_level": 1
}
```

#### 批量导入单词
```http
POST /api/vocabulary/groups/{group_id}/words/batch
```

## 前端页面

### 主要组件

1. **VocabularyManagement.vue** - 词库管理主页面
2. **LibraryDetailPanel.vue** - 词库详情面板
3. **LibraryModal.vue** - 词库创建/编辑模态框
4. **GroupDetailPanel.vue** - 词组详情面板
5. **GroupModal.vue** - 词组创建/编辑模态框
6. **WordModal.vue** - 单词创建/编辑模态框
7. **BatchImportModal.vue** - 批量导入模态框

### 功能特性

- 响应式设计，支持移动端
- 实时搜索和筛选
- 拖拽排序
- 批量操作
- 数据导入导出
- 标签管理

## 部署说明

### 后端部署

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 初始化数据库：
```bash
python init_vocabulary_db.py
```

3. 启动服务：
```bash
python run.py
```

### 前端部署

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 开发模式：
```bash
npm run dev
```

3. 生产构建：
```bash
npm run build
```

## 使用示例

### 创建词库
1. 访问词库管理页面
2. 点击"创建词库"按钮
3. 填写词库信息（名称、描述、标签、难度等级）
4. 保存

### 添加词组
1. 选择词库
2. 在词库详情面板中点击"添加词组"
3. 填写词组信息
4. 保存

### 添加单词
1. 选择词组
2. 在词组详情面板中点击"添加单词"
3. 填写单词的完整信息
4. 保存

### 批量导入
1. 准备CSV格式的单词数据
2. 选择目标词组
3. 点击"批量导入"
4. 上传CSV文件
5. 确认导入

## 扩展功能

### 计划中的功能
- [ ] 词汇学习进度跟踪
- [ ] 智能推荐系统
- [ ] 语音朗读功能
- [ ] 词汇测试生成
- [ ] 学习统计分析
- [ ] 多语言支持
- [ ] 词汇卡片模式
- [ ] 社区分享功能

### 技术优化
- [ ] 缓存优化
- [ ] 全文搜索
- [ ] 数据同步
- [ ] 离线支持
- [ ] 性能监控

## 贡献指南

欢迎提交Issue和Pull Request来改进词库管理系统！

## 许可证

MIT License