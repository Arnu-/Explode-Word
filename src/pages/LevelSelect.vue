<template>
  <div class="level-select-page">
    <!-- 添加半透明蒙版底 -->
    <div class="page-overlay"></div>
    <!-- 页面标题栏 -->
    <!-- <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="navigateToHome">
          <img src="../../assets/CodeBubbyAssets/20_13/45.svg" alt="返回" />
        </button>
        <h1 class="page-title">选择关卡</h1>
      </div>
      
      <div class="header-right">
        <div class="user-level">
          <div class="level-badge">
            <span>42</span>
          </div>
          <span class="level-text">大师级</span>
        </div>
        
        <div class="coins">
          <img src="../../assets/CodeBubbyAssets/20_13/46.svg" alt="金币" class="coin-icon" />
          <span class="coin-amount">3,250</span>
        </div>
        
        <button class="settings-button">
          <img src="../../assets/CodeBubbyAssets/20_13/47.svg" alt="设置" />
        </button>
      </div>
    </div> -->

    <!-- 关卡网格 (固定3x3布局) -->
    <div class="levels-grid content-layer">
      <LevelCard
        v-for="lvl in displayedLevels"
        :key="lvl.id"
        :level="lvl"
        :selected="selected?.id === lvl.id"
        @select="lvl.status !== 'coming-soon' ? selected = lvl : null"
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
      <div class="progress-header">
        <span class="progress-label">游戏进度</span>
        <span class="progress-value">24/48</span>
      </div>
      
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      
      <div class="progress-stats">
        <div class="stars-stat">
          <div class="stars-icons">
            <img src="../../assets/CodeBubbyAssets/20_13/1.svg" alt="星星" />
            <img src="../../assets/CodeBubbyAssets/20_13/2.svg" alt="星星" />
            <img src="../../assets/CodeBubbyAssets/20_13/3.svg" alt="星星" />
          </div>
          <div class="stars-count">{{ collectedStars }}/{{ totalStars }}</div>
          <div class="stars-label">收集星星</div>
        </div>
        
        <div class="achievement-stat">
          <div class="achievement-icon">
            <img src="../../assets/CodeBubbyAssets/20_13/4.svg" alt="成就" />
          </div>
          <div class="achievement-count">{{ achievements }}/{{ achievementsTotal }}</div>
          <div class="achievement-label">成就完成</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import LevelCard from '@/components/levels/LevelCard.vue';
import PaginationDots from '@/components/levels/PaginationDots.vue';
import LevelDetailsPanel from '@/components/levels/LevelDetailsPanel.vue';

const router = useRouter();

function navigateToHome() {
  router.push('/');
}

// mock 数据，可后续替换为接口/存储
const allLevels = ref([
  { id: 1, title: '魔法森林挑战', difficulty: '简单', status: 'completed', stars: 3, estTimeMin: 6,
    tasks: [{text:'收集至少15个魔法宝石',done:true},{text:'在60秒内完成关卡',done:false},{text:'不损失任何生命值',done:true}],
    bestScore: 12450, lastPlayedAgo: '2天前', rewardCoin: 12450 },
  { id: 2, title: '魔法森林挑战', difficulty: '简单', status: 'completed', stars: 2, estTimeMin: 6, 
    tasks: [{text:'收集至少10个魔法宝石',done:true},{text:'在90秒内完成关卡',done:true},{text:'不损失任何生命值',done:false}],
    bestScore: 9820, lastPlayedAgo: '5天前', rewardCoin: 10800 },
  { id: 3, title: '魔法森林挑战', difficulty: '中等', status: 'available',  stars: 1, estTimeMin: 7, 
    tasks: [{text:'收集至少20个魔法宝石',done:true},{text:'在120秒内完成关卡',done:false},{text:'不损失任何生命值',done:false}],
    bestScore: 7650, lastPlayedAgo: '7天前', rewardCoin: 11500 },
  { id: 4, title: '魔法森林挑战', difficulty: '中等', status: 'available',  stars: 0, estTimeMin: 8, 
    tasks: [{text:'收集至少25个魔法宝石',done:false},{text:'在150秒内完成关卡',done:false},{text:'不损失任何生命值',done:false}],
    bestScore: null, lastPlayedAgo: '—', rewardCoin: 12450 },
  { id: 5, title: '魔法森林挑战', difficulty: '中等', status: 'available',  stars: 0, estTimeMin: 8, 
    tasks: [{text:'收集至少30个魔法宝石',done:false},{text:'在180秒内完成关卡',done:false},{text:'不损失任何生命值',done:false}],
    bestScore: null, lastPlayedAgo: '—', rewardCoin: 12450 },
  { id: 6, title: '魔法森林挑战', difficulty: '困难', status: 'available',  stars: 0, estTimeMin: 9, 
    tasks: [{text:'收集至少35个魔法宝石',done:false},{text:'在210秒内完成关卡',done:false},{text:'不损失任何生命值',done:false}],
    bestScore: null, lastPlayedAgo: '—', rewardCoin: 14800 },
  { id: 7, title: '魔法森林挑战', difficulty: '未知', status: 'locked',    stars: 0, estTimeMin: 9, 
    tasks: [{text:'???',done:false},{text:'???',done:false},{text:'???',done:false}],
    bestScore: null, lastPlayedAgo: '—', rewardCoin: 16000 },
  { id: 8, title: '魔法森林挑战', difficulty: '未知', status: 'locked',    stars: 0, estTimeMin: 9, 
    tasks: [{text:'???',done:false},{text:'???',done:false},{text:'???',done:false}],
    bestScore: null, lastPlayedAgo: '—', rewardCoin: 16000 },
  // 更多关卡...
]);

// 创建固定的3x3布局，不足9个的用"待开放"占位
const fixedGridSize = 9; // 3x3布局
const displayedLevels = computed(() => {
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

// 顶部统计（示例）
const totalStars = 144;
const collectedStars = computed(() => allLevels.value.reduce((a,l)=>a+l.stars,0));
const achievements = 18;
const achievementsTotal = 30;
const progressPercent = computed(() => Math.min(100, Math.round((collectedStars.value/totalStars)*100)));

function goPage(p){ page.value = p; selected.value = pagedLevels.value[0] ?? null; }
function prevPage(){ if(page.value>1) goPage(page.value-1); }
function nextPage(){ if(page.value<totalPages.value) goPage(page.value+1); }

function startLevel(lvl){
  // TODO: 触发游戏开始（路由跳转或事件）
  console.log('start level:', lvl.id);
  alert(`开始游戏：${lvl.title} (关卡 ${lvl.id})`);
}

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
  justify-content: space-between;
  padding: 0 24px;
  margin-bottom: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-button {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.back-button img {
  width: 14px;
  height: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-level {
  display: flex;
  align-items: center;
  gap: 8px;
}

.level-badge {
  width: 32px;
  height: 32px;
  background: linear-gradient(90deg, #FACC15 0%, #F97316 100%);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.level-text {
  font-size: 14px;
}

.coins {
  display: flex;
  align-items: center;
  gap: 8px;
}

.coin-icon {
  width: 16px;
  height: 16px;
}

.coin-amount {
  font-size: 16px;
  font-weight: 700;
}

.settings-button {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.settings-button img {
  width: 16px;
  height: 16px;
}

/* 进度条区域 */
.progress-container {
  margin: 32px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-header);
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

.progress-bar {
  height: 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-full);
  overflow: hidden;
  margin-bottom: 24px;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-progress);
  border-radius: var(--border-radius-full);
  position: relative;
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

.progress-stats {
  display: flex;
  justify-content: space-between;
}

.stars-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stars-icons {
  display: flex;
  gap: 0;
}

.stars-icons img {
  width: 23px;
  height: 20px;
}

.stars-count {
  font-size: 14px;
  font-weight: 700;
  margin-top: 4px;
  color: #ffffff; /* 白色字体 */
}

.stars-label {
  font-size: 12px;
  color: #cbd5e1; /* 浅色字体 */
}

.achievement-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.achievement-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(90deg, #34D399 0%, #14B8A6 100%);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.achievement-icon img {
  width: 23px;
  height: 20px;
}

.achievement-count {
  font-size: 14px;
  font-weight: 700;
  margin-top: 4px;
  color: #ffffff; /* 白色字体 */
}

.achievement-label {
  font-size: 12px;
  color: #cbd5e1; /* 浅色字体 */
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
