<template>
  <div class="level-select-page">
    <!-- 添加半透明蒙版底 -->
    <div class="page-overlay"></div>
    
    <!-- 页面标题栏 - 简化版，移除用户信息到外层框架 -->
    <div class="page-header content-layer">
      <div class="header-center">
        <h1 class="page-title">选择关卡</h1>
      </div>
    </div>

    <!-- 词库信息栏 -->
    <div class="vocabulary-info content-layer">
      <div class="vocabulary-current" v-if="currentLibrary">
        <div class="vocabulary-label">当前词库:</div>
        <div class="vocabulary-name">{{ currentLibrary.name }}</div>
        <div class="vocabulary-stats">
          <span>{{ currentLibrary.groups_count || 0 }}个词组</span>
          <span>{{ currentLibrary.total_words_count || 0 }}个单词</span>
        </div>
      </div>
      <div class="vocabulary-current" v-else>
        <div class="vocabulary-label">当前词库:</div>
        <div class="vocabulary-name">未选择</div>
      </div>
      <button @click="showLibrarySelectModal = true" class="switch-library-btn">
        切换词库
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container content-layer">
      <div class="loading-text">加载关卡数据中...</div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container content-layer">
      <div class="error-text">{{ error }}</div>
      <button @click="loadLevels" class="retry-button">重试</button>
    </div>

    <!-- 关卡网格 (固定3x3布局) -->
    <div v-else class="levels-grid content-layer">
      <LevelCard
        v-for="lvl in displayedLevels"
        :key="lvl.id"
        :level="lvl"
        :selected="selected?.id === lvl.id"
        @select="lvl.status !== 'coming-soon' && lvl.status !== 'locked' ? startLevel(lvl) : (lvl.status !== 'coming-soon' ? selected = lvl : null)"
        @mouseover="lvl.status === 'locked' || lvl.status !== 'coming-soon' ? handleMouseOver($event, lvl) : null"
        @mouseleave="hoveredLevel = null"
      />
    </div>

    <!-- 浮动详情面板 -->
    <LevelDetailsPanel 
      v-if="hoveredLevel" 
      :level="hoveredLevel" 
      @start="startLevel(hoveredLevel)"
      class="floating-panel"
      :style="panelPosition"
    />

    <!-- 进度条区域 -->
    <div class="progress-container content-layer">
      <!-- 游戏进度条 -->
      <div class="progress-section">
        <div class="progress-header">
          <span class="progress-label">游戏进度</span>
          <span class="progress-value">{{ userProgress?.completed_levels || 0 }}/{{ userProgress?.total_levels || 0 }}</span>
        </div>
        
        <div class="progress-bar-container">
          <div class="progress-bar">
            <div class="progress-fill game-progress" :style="{ width: progressPercent + '%' }"></div>
          </div>
          <div class="progress-icon stars-icons">
            <img :src="star1Icon" alt="星星" />
            <img :src="star2Icon" alt="星星" />
            <img :src="star3Icon" alt="星星" />
          </div>
        </div>
      </div>
      
      <!-- 游戏成就条 -->
      <div class="progress-section">
        <div class="progress-header">
          <span class="progress-label">游戏成就</span>
          <span class="progress-value">{{ achievements }}/{{ achievementsTotal }}</span>
        </div>
        
        <div class="progress-bar-container">
          <div class="progress-bar">
            <div class="progress-fill achievement-progress" :style="{ width: achievementPercent + '%' }"></div>
          </div>
          <div class="progress-icon achievement-icon">
            <img :src="achievementIcon" alt="成就" />
          </div>
        </div>
      </div>
    </div>

    <!-- 词库选择弹窗 -->
    <LibrarySelectModal
      v-if="showLibrarySelectModal"
      @close="showLibrarySelectModal = false"
      @select="handleLibrarySelect"
      @create-library="handleCreateLibrary"
    />

    <!-- 创建词库弹窗 -->
    <LibraryModal
      v-if="showLibraryModal"
      @close="showLibraryModal = false"
      @saved="handleLibraryCreated"
    />

  </div>
</template>

<script setup>
import { computed, ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import LevelCard from '@/components/levels/LevelCard.vue';
import PaginationDots from '@/components/levels/PaginationDots.vue';
import LevelDetailsPanel from '@/components/levels/LevelDetailsPanel.vue';
import LibrarySelectModal from '@/components/vocabulary/LibrarySelectModal.vue';
import LibraryModal from '@/components/vocabulary/LibraryModal.vue';
import levelService from '@/services/levelService.js';
import { vocabularyApi } from '@/utils/vocabularyApi.js';

// 导入图片资源
import star1Icon from '@/assets/CodeBubbyAssets/20_13/1.svg';
import star2Icon from '@/assets/CodeBubbyAssets/20_13/2.svg';
import star3Icon from '@/assets/CodeBubbyAssets/20_13/3.svg';
import achievementIcon from '@/assets/CodeBubbyAssets/20_13/4.svg';

const router = useRouter();

// 数据状态
const allLevels = ref([]);
const loading = ref(false);
const error = ref(null);
const userProgress = ref(null);

// 词库相关状态
const currentLibrary = ref(null);
const showLibrarySelectModal = ref(false);
const showLibraryModal = ref(false);

// 创建固定的3x3布局，基于当前词库的词组生成关卡
const fixedGridSize = 9; // 3x3布局
const displayedLevels = computed(() => {
  if (!currentLibrary.value) {
    // 如果没有选择词库，显示占位卡片
    return Array.from({ length: fixedGridSize }, (_, index) => ({
      id: `no-library-${index + 1}`,
      title: '请选择词库',
      difficulty: '未知',
      status: 'locked',
      stars: 0,
      estTimeMin: 0,
      tasks: [{text:'请先选择词库',done:false},{text:'请先选择词库',done:false},{text:'请先选择词库',done:false}],
      bestScore: null,
      lastPlayedAgo: '—',
      rewardCoin: 0
    }));
  }

  const levels = [...allLevels.value];
  // 如果关卡数量不足9个，添加"待开放"占位卡片
  while (levels.length < fixedGridSize) {
    levels.push({
      id: `coming-soon-${levels.length + 1}`,
      title: '待开放',
      difficulty: '未知',
      status: 'coming-soon',
      stars: 0,
      estTimeMin: 0,
      tasks: [{text:'敬请期待',done:false},{text:'敬请期待',done:false},{text:'敬请期待',done:false}],
      bestScore: null,
      lastPlayedAgo: '—',
      rewardCoin: 0
    });
  }
  return levels.slice(0, fixedGridSize); // 只显示前9个
});

const selected = ref(allLevels.value[3]); // 默认选中 4 号卡，贴合设计截图
const hoveredLevel = ref(null);
const hoveredCardRef = ref(null);

// 计算浮动面板位置
const panelPosition = computed(() => {
  if (!hoveredCardRef.value) return {};
  
  // 获取卡片元素的位置和尺寸
  const cardRect = hoveredCardRef.value.getBoundingClientRect();
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;
  
  // 面板宽度
  const panelWidth = 400;
  const panelHeight = 300; // 估计高度
  
  // 判断卡片在屏幕的位置
  const isRightHalf = cardRect.left + cardRect.width/2 > windowWidth/2;
  const isBottomHalf = cardRect.top + cardRect.height/2 > windowHeight/2;
  
  // 根据卡片位置决定面板出现的方向
  let left, top;
  
  if (isRightHalf) {
    // 卡片在右侧，面板显示在左侧
    left = `${cardRect.left - panelWidth - 10}px`;
  } else {
    // 卡片在左侧，面板显示在右侧
    left = `${cardRect.right + 10}px`;
  }
  
  // 垂直方向上居中对齐
  top = `${cardRect.top + cardRect.height/2 - panelHeight/2}px`;
  
  // 确保面板不会超出屏幕
  if (parseFloat(left) < 0) {
    left = '10px';
  } else if (parseFloat(left) + panelWidth > windowWidth) {
    left = `${windowWidth - panelWidth - 10}px`;
  }
  
  if (parseFloat(top) < 0) {
    top = '10px';
  } else if (parseFloat(top) + panelHeight > windowHeight) {
    top = `${windowHeight - panelHeight - 10}px`;
  }
  
  return { left, top };
});

// 加载关卡数据
const loadLevels = async () => {
  if (!currentLibrary.value) {
    // 如果没有选择词库，清空关卡数据
    allLevels.value = [];
    return;
  }

  try {
    loading.value = true;
    error.value = null;
    
    // 获取当前词库的词组列表，每个词组对应一个关卡
    const groupsResponse = await vocabularyApi.getGroups(currentLibrary.value.id);
    console.log('词组API响应:', groupsResponse);
    
    if (groupsResponse.success) {
      // 处理不同的数据格式
      let groupsData = groupsResponse.data
      if (groupsData && typeof groupsData === 'object') {
        // 如果data是对象，可能包含groups字段
        if (groupsData.groups && Array.isArray(groupsData.groups)) {
          groupsData = groupsData.groups
        } else if (Array.isArray(groupsData)) {
          // 如果data本身就是数组
          groupsData = groupsData
        } else {
          // 如果都不是，设为空数组
          groupsData = []
        }
      } else {
        groupsData = []
      }
      
      // 将词组转换为关卡数据
      allLevels.value = groupsData.map((group, index) => ({
        id: group.id,
        title: group.name,
        difficulty: getDifficultyText(group.difficulty_level),
        status: 'available', // 所有关卡都可用
        stars: 0, // 可以根据用户进度设置
        estTimeMin: Math.max(5, Math.ceil((group.words_count || 10) / 2)), // 根据单词数量估算时间
        tasks: [
          { text: `学习 ${group.words_count || 0} 个单词`, done: false },
          { text: '完成词汇测试', done: false },
          { text: '达到80%正确率', done: false }
        ],
        bestScore: null,
        lastPlayedAgo: '—',
        rewardCoin: (group.words_count || 10) * 10, // 根据单词数量计算奖励
        groupId: group.id, // 保存词组ID用于游戏
        wordsCount: group.words_count || 0
      }));
    }
    
    // 获取用户进度
    const progressResponse = await levelService.getUserProgress();
    userProgress.value = progressResponse?.progress || progressResponse || {
      total_stars: 0,
      completed_levels: 0,
      total_levels: allLevels.value.length,
      completion_percentage: 0
    };
    
  } catch (err) {
    console.error('加载关卡数据失败:', err);
    error.value = err.message || '加载失败';
    allLevels.value = [];
  } finally {
    loading.value = false;
  }
};

// 计算进度统计
const collectedStars = computed(() => {
  if (userProgress.value) {
    return userProgress.value.total_stars;
  }
  return allLevels.value.reduce((a, l) => a + l.stars, 0);
});

const progressPercent = computed(() => {
  if (userProgress.value) {
    return userProgress.value.progress_percent;
  }
  return 0;
});

const achievements = computed(() => {
  if (userProgress.value) {
    return userProgress.value.achievements;
  }
  return 18;
});

const achievementsTotal = computed(() => {
  if (userProgress.value) {
    return userProgress.value.achievements_total;
  }
  return 30;
});

const achievementPercent = computed(() => {
  if (userProgress.value) {
    return userProgress.value.achievement_percent;
  }
  return 60;
});

function goPage(p){ page.value = p; selected.value = pagedLevels.value[0] ?? null; }
function prevPage(){ if(page.value>1) goPage(page.value-1); }
function nextPage(){ if(page.value<totalPages.value) goPage(page.value+1); }

async function startLevel(lvl) {
  // 检查是否选择了词库
  if (!currentLibrary.value) {
    showLibrarySelectModal.value = true;
    return;
  }

  // 检查关卡状态
  if (lvl.status === 'locked' || lvl.status === 'coming-soon') {
    return;
  }

  try {
    // 跳转到游戏页面，使用关卡ID作为路由参数，其他信息作为查询参数
    console.log('开始游戏:', {
      levelId: lvl.id,
      libraryId: currentLibrary.value.id,
      groupId: lvl.groupId,
      levelTitle: lvl.title
    });
    
    router.push({ 
      name: 'game', 
      params: {
        levelId: lvl.id
      },
      query: {
        libraryId: currentLibrary.value.id,
        groupId: lvl.groupId,
        levelTitle: lvl.title
      }
    });
  } catch (err) {
    console.error('启动游戏失败:', err);
  }
}

// 词库相关方法
const checkAndLoadLibrary = async () => {
  // 检查本地存储中是否有选择的词库
  const savedLibraryId = localStorage.getItem('selectedLibraryId');
  
  if (savedLibraryId) {
    try {
      const response = await vocabularyApi.getLibrary(savedLibraryId);
      console.log('加载保存的词库响应:', response);
      
      if (response.success && response.data) {
        currentLibrary.value = response.data;
        await loadLevels();
        return;
      }
    } catch (err) {
      console.error('加载保存的词库失败:', err);
      localStorage.removeItem('selectedLibraryId');
    }
  }
  
  // 如果没有保存的词库或加载失败，显示选择弹窗
  showLibrarySelectModal.value = true;
};

const handleLibrarySelect = async (library) => {
  currentLibrary.value = library;
  localStorage.setItem('selectedLibraryId', library.id.toString());
  showLibrarySelectModal.value = false;
  await loadLevels();
};

const handleCreateLibrary = () => {
  showLibrarySelectModal.value = false;
  showLibraryModal.value = true;
};

const handleLibraryCreated = (library) => {
  showLibraryModal.value = false;
  showLibrarySelectModal.value = true; // 重新显示选择弹窗
};

// 获取难度文本
const getDifficultyText = (level) => {
  const texts = ['', '初级', '中级', '中高级', '高级', '专家级'];
  return texts[level] || '未知';
};

// 组件挂载时检查并加载词库
onMounted(() => {
  checkAndLoadLibrary();
});

// 处理鼠标悬停事件
function handleMouseOver(event, lvl) {
  if (lvl.status === 'locked' )
{
  return;
}
  hoveredLevel.value = lvl;
  // 获取当前悬停的卡片元素
  hoveredCardRef.value = event.currentTarget;
}
</script>

<style scoped>
@import '@/assets/theme.css';

.floating-panel {
  position: fixed;
  z-index: 100;
  pointer-events: auto; /* 允许点击面板上的元素 */
  transition: all 0.3s ease;
  width: 400px; /* 设置合适的宽度 */
  max-width: 90vw; /* 响应式处理 */
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* 确保内容在蒙版上方 */
.content-layer {
  position: relative;
  z-index: 1;
}

.level-select-page {
  min-height: 100vh;
  color: var(--color-text-primary);
  position: relative;
  padding-top: 1rem;
  overflow: hidden; /* 防止蒙版溢出 */
}

/* 半透明蒙版底 */
.page-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
  z-index: 0;
  border-radius: var(--border-radius-large);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.1);
}

/* 页面标题栏 */
.page-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  margin-bottom: 1rem;
}

.header-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 词库信息栏 */
.vocabulary-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-header);
}

.vocabulary-current {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vocabulary-label {
  font-size: 14px;
  color: #cbd5e1;
  font-weight: 500;
}

.vocabulary-name {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
}

.vocabulary-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #94a3b8;
}

.switch-library-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius-medium);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.switch-library-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  text-align: center;
  background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 进度条区域 */
.progress-container {
  margin: 32px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-header);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.progress-section {
  display: flex;
  flex-direction: column;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  color: #cbd5e1; /* 浅色字体 */
}

.progress-value {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff; /* 白色字体 */
}

.progress-bar-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  width: 100%;
}

.progress-bar {
  height: 8px; /* 更窄的进度条 */
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-full);
  overflow: hidden;
  width: calc(100% - 60px); /* 固定宽度，减去图标宽度和间距 */
}

.progress-fill {
  height: 100%;
  border-radius: var(--border-radius-full);
  position: relative;
}

.game-progress {
  background: linear-gradient(90deg, #3b82f6, #8b5cf6); /* 蓝紫渐变 */
}

.achievement-progress {
  background: linear-gradient(90deg, #34D399, #14B8A6); /* 绿色渐变 */
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  opacity: 0.5;
}

.progress-icon {
  display: flex;
  align-items: center;
  min-width: 60px; /* 固定宽度，确保两个图标区域一致 */
  justify-content: center;
}

.stars-icons {
  display: flex;
  gap: 0;
}

.stars-icons img {
  width: 20px;
  height: 18px;
}

.achievement-icon {
  width: 28px;
  height: 28px;
  background: linear-gradient(90deg, #34D399 0%, #14B8A6 100%);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.achievement-icon img {
  width: 16px;
  height: 16px;
}

/* 关卡网格 */
.levels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 0 32px;
  margin-bottom: 32px;
}

/* 底部导航栏已移至App.vue */

@media (max-width: 1200px) {
  .levels-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 加载和错误状态样式 */
.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  padding: 32px;
}

.loading-text {
  font-size: 18px;
  color: #cbd5e1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.error-container {
  background: rgba(239, 68, 68, 0.1);
  border-radius: var(--border-radius-large);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.error-text {
  font-size: 16px;
  color: #fca5a5;
  margin-bottom: 16px;
  text-align: center;
}

.retry-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  border-radius: var(--border-radius-medium);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.retry-button:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .levels-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-stats {
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }
}
</style>
