<template>
  <div class="level-select-page">
    <!-- 顶部导航栏 -->
    <header class="header">
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
    </header>

    <!-- 进度条区域 -->
    <div class="progress-container">
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

    <!-- 关卡网格 -->
    <div class="levels-grid">
      <LevelCard
        v-for="lvl in pagedLevels"
        :key="lvl.id"
        :level="lvl"
        :selected="selected?.id === lvl.id"
        @select="selected = lvl"
      />
    </div>

    <!-- 分页 -->
    <PaginationDots 
      :total="totalPages" 
      :current="page" 
      @change="goPage"
      @prev="prevPage"
      @next="nextPage"
    />

    <!-- 底部详情面板 -->
    <LevelDetailsPanel v-if="selected" :level="selected" @start="startLevel(selected)"/>

    <!-- 底部导航栏 -->
    <nav class="bottom-nav">
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/48.svg" alt="首页" class="nav-icon" />
        <span class="nav-text">首页</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/49.svg" alt="排行榜" class="nav-icon" />
        <span class="nav-text">排行榜</span>
      </div>
      <div class="nav-item active">
        <img src="../../assets/CodeBubbyAssets/20_13/50.svg" alt="关卡" class="nav-icon" />
        <span class="nav-text">关卡</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/51.svg" alt="商店" class="nav-icon" />
        <span class="nav-text">商店</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/52.svg" alt="个人" class="nav-icon" />
        <span class="nav-text">个人</span>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
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

const page = ref(1);
const pageSize = 6;
const totalPages = computed(() => Math.ceil(allLevels.value.length / pageSize));
const pagedLevels = computed(() => allLevels.value.slice((page.value-1)*pageSize, page.value*pageSize));

const selected = ref(allLevels.value[3]); // 默认选中 4 号卡，贴合设计截图

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
</script>

<style scoped>
@import '@/assets/theme.css';

.level-select-page {
  min-height: 100vh;
  background: var(--gradient-background);
  color: var(--color-text-primary);
  padding-bottom: var(--footer-height);
  position: relative;
}

/* 顶部导航栏 */
.header {
  height: var(--header-height);
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
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
  color: var(--color-text-secondary);
}

.progress-value {
  font-size: 14px;
  font-weight: 700;
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
}

.stars-label {
  font-size: 12px;
  color: var(--color-text-secondary);
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
}

.achievement-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}

/* 关卡网格 */
.levels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 0 32px;
  margin-bottom: 32px;
}

/* 底部导航栏 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--footer-height);
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: space-between;
  padding: 0 24px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 100%;
}

.nav-icon {
  width: 18px;
  height: 16px;
  margin-bottom: 4px;
}

.nav-text {
  font-size: 12px;
  color: #9CA3AF;
}

.nav-item.active .nav-text {
  color: #60A5FA;
}

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
