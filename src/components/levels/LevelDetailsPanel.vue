<template>
  <section class="panel">
    <div class="panel-content">
      <div class="left-content">
        <h2 class="title">{{ level.title }}</h2>
        
        <div class="meta">
          <span class="chip" :class="difficultyClass">{{ level.difficulty }}难度</span>
          <span class="time">预计时间: {{ level.estTimeMin }}分钟</span>
        </div>

        <div class="score-section">
          <div class="score-label">历史最高分</div>
          <div class="score-value">{{ level.bestScore ? level.bestScore.toLocaleString() : '—' }}</div>
          <div class="stars">
            <StarRating :value="level.stars" />
          </div>
        </div>

        <div class="tasks">
          <div class="task" v-for="(task, idx) in level.tasks" :key="idx">
            <img 
              :src="task.done 
                ? '../../assets/CodeBubbyAssets/20_13/42.svg' 
                : '../../assets/CodeBubbyAssets/20_13/43.svg'" 
              class="task-icon" 
              :alt="task.done ? '已完成' : '未完成'"
            />
            <span class="task-text">{{ task.text }}</span>
          </div>
        </div>
      </div>

      <div class="right-content">
        <div class="last-played">上次游玩: {{ level.lastPlayedAgo }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import StarRating from './StarRating.vue';
import { computed } from 'vue';

const props = defineProps({ level: Object });

const difficultyClass = computed(() => {
  switch(props.level.difficulty) {
    case '简单': return 'easy';
    case '中等': return 'medium';
    case '困难': return 'hard';
    default: return 'unknown';
  }
});

defineEmits(['start']);
</script>

<style scoped>
.panel {
  margin-top: 12px;
  border-radius: var(--border-radius-large);
  background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); /* 蓝绿渐变色背景 */
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-header);
  outline: 1px solid var(--color-border);
  outline-offset: -1px;
  backdrop-filter: blur(8px); /* 添加模糊效果 */
  animation: fadeIn 0.2s ease-in-out; /* 添加淡入动画 */
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.panel-content {
  padding: 25px;
  display: flex;
  justify-content: space-between;
}

.left-content {
  flex: 1;
}

.title {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff; /* 标题改为白色 */
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.chip {
  font-size: 12px;
  padding: 5px 8px;
  border-radius: var(--border-radius-full);
}

.chip.easy {
  background: var(--color-easy-bg);
  color: var(--color-easy-text);
}

.chip.medium {
  background: var(--color-medium-bg);
  color: var(--color-medium-text);
}

.chip.hard {
  background: var(--color-hard-bg);
  color: var(--color-hard-text);
}

.time {
  font-size: 14px;
  color: #cbd5e1; /* 更亮的浅灰色文本 */
}

.score-section {
  margin-bottom: 16px;
}

.score-label {
  font-size: 14px;
  margin-bottom: 4px;
  color: #e2e8f0; /* 浅灰色文本 */
}

.score-value {
  font-size: 14px;
  font-weight: 700;
  text-align: right;
  position: absolute;
  right: 25px;
  margin-top: -20px;
  color: #ffffff; /* 白色文本 */
}

.stars {
  margin-top: 4px;
}

.tasks {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-icon {
  width: 14px;
  height: 14px;
}

.task-text {
  font-size: 14px;
  color: #e2e8f0; /* 浅灰色文本 */
}

.right-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.start-button {
  padding: 15px 30px;
  border-radius: var(--border-radius-full);
  border: none;
  background: linear-gradient(135deg, #f97316 0%, #ec4899 100%); /* 橙粉渐变色按钮 */
  color: white;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  box-shadow: var(--shadow-button);
  transition: transform 0.2s;
  pointer-events: auto; /* 确保按钮可点击 */
  z-index: 101; /* 确保按钮在最上层 */
}

.start-button:hover {
  transform: translateY(-2px);
}

.last-played {
  font-size: 12px;
  color: #cbd5e1; /* 更亮的浅灰色文本 */
}
</style>
