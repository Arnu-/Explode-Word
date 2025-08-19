<template>
  <div class="section-select-page">
    <!-- 添加半透明蒙版底 -->
    <div class="page-overlay"></div>
    
    <!-- 页面标题栏 -->
    <div class="page-header">
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
    </div>

    <!-- 章节选择区域 -->
    <div class="sections-container">
      <!-- 左箭头 -->
      <button class="nav-arrow left-arrow" @click="prevSection" :disabled="currentPage === 0">
        <div class="arrow-icon">&#10094;</div>
      </button>
      
      <!-- 章节卡片 -->
      <div class="sections-grid">
        <div 
          v-for="section in displayedSections" 
          :key="section.id" 
          class="section-card"
          @click="selectSection(section)"
        >
          <div class="card-image">
            <img :src="section.image" alt="章节图片" />
          </div>
          <div class="card-title">{{ section.title }}</div>
        </div>
      </div>
      
      <!-- 右箭头 -->
      <button class="nav-arrow right-arrow" @click="nextSection" :disabled="currentPage >= Math.ceil(sections.length / pageSize) - 1">
        <div class="arrow-icon">&#10095;</div>
      </button>
    </div>

    <!-- 底部导航栏 -->
    <div class="bottom-nav">
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/48.svg" alt="首页" />
        <span>首页</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/49.svg" alt="排行榜" />
        <span>排行榜</span>
      </div>
      <div class="nav-item active">
        <img src="../../assets/CodeBubbyAssets/20_13/50.svg" alt="关卡" />
        <span>关卡</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/51.svg" alt="商店" />
        <span>商店</span>
      </div>
      <div class="nav-item">
        <img src="../../assets/CodeBubbyAssets/20_13/52.svg" alt="个人" />
        <span>个人</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { chapterImages } from '@/assets/chapter-image';

const router = useRouter();

// 导航到首页
function navigateToHome() {
  router.push('/');
}

// 章节数据
const sections = ref([
  { 
    id: 1, 
    title: '第一关，小试牛刀', 
    image: chapterImages.tomJerry,
    levels: [1, 2, 3, 4]
  },
  { 
    id: 2, 
    title: '第二关，小试牛刀', 
    image: chapterImages.tomJerry,
    levels: [5, 6, 7, 8]
  },
  { 
    id: 3, 
    title: '第三关，关公在世', 
    image: chapterImages.tomJerry,
    levels: [9, 10, 11, 12]
  },
  { 
    id: 4, 
    title: '第四关，挑战极限', 
    image: chapterImages.tomJerry,
    levels: [13, 14, 15, 16]
  },
  { 
    id: 5, 
    title: '第五关，最终决战', 
    image: chapterImages.tomJerry,
    levels: [17, 18, 19, 20]
  }
]);

// 分页相关
const currentPage = ref(0);
const pageSize = 3; // 每页显示3个章节

// 当前页显示的章节
const displayedSections = computed(() => {
  const start = currentPage.value * pageSize;
  const end = start + pageSize;
  return sections.value.slice(start, end);
});

// 翻页函数
function prevSection() {
  if (currentPage.value > 0) {
    currentPage.value--;
  }
}

function nextSection() {
  if (currentPage.value < Math.ceil(sections.value.length / pageSize) - 1) {
    currentPage.value++;
  }
}

// 选择章节
function selectSection(section) {
  // 这里可以跳转到关卡选择页面，并传递章节ID
  console.log('选择章节:', section.id);
  router.push({
    path: '/levels',
    query: { sectionId: section.id }
  });
}
</script>

<style scoped>
@import '@/assets/theme.css';

.section-select-page {
  min-height: 100vh;
  color: var(--color-text-primary);
  position: relative;
  padding-top: 1rem;
  overflow: hidden; /* 防止蒙版溢出 */
  display: flex;
  flex-direction: column;
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
  position: relative;
  z-index: 1;
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

/* 章节选择区域 */
.sections-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.sections-grid {
  display: flex;
  gap: 24px;
  justify-content: center;
  max-width: 1200px;
  margin: 0 auto;
}

.section-card {
  width: 260px;
  height: 380px;
  background: rgba(55, 48, 163, 0.6);
  border-radius: var(--border-radius-medium);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--color-border);
}

.section-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
}

.card-image {
  flex: 1;
  background: #6366f1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-title {
  padding: 16px;
  text-align: center;
  font-weight: 600;
  font-size: 16px;
}

/* 导航箭头 */
.nav-arrow {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: var(--border-radius-full);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-arrow:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.left-arrow {
  left: 20px;
}

.right-arrow {
  right: 20px;
}

.arrow-icon {
  font-size: 24px;
  color: #312E81;
  font-weight: bold;
}

/* 底部导航栏 */
.bottom-nav {
  height: 60px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-around;
  align-items: center;
  position: relative;
  z-index: 10;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  cursor: pointer;
  transition: color 0.3s;
}

.nav-item img {
  width: 24px;
  height: 24px;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.nav-item:hover {
  color: white;
}

.nav-item:hover img {
  opacity: 1;
}

.nav-item.active {
  color: white;
}

.nav-item.active img {
  opacity: 1;
}

@media (max-width: 1024px) {
  .sections-grid {
    gap: 16px;
  }
  
  .section-card {
    width: 220px;
    height: 320px;
  }
}

@media (max-width: 768px) {
  .sections-grid {
    gap: 12px;
  }
  
  .section-card {
    width: 180px;
    height: 280px;
  }
  
  .nav-arrow {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 640px) {
  .sections-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .section-card {
    width: 260px;
    height: 380px;
  }
}
</style>