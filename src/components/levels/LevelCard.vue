<template>
  <button
    class="card"
    :class="[{ 
      selected, 
      locked: level.status === 'locked',
      'coming-soon': level.status === 'coming-soon',
      active: selected
    }]"
    @click="$emit('select', level)"
    @mouseover="$emit('mouseover', $event)"
    @mouseleave="$emit('mouseleave')"
    :disabled="level.status === 'locked' || level.status === 'coming-soon'"
  >
    <div class="card-content">
      <div class="top">
        <span class="index">{{ level.id }}</span>
        <span class="chip" :class="difficultyClass">{{ level.difficulty }} ({{ difficultyClass }})</span>
      </div>

      <div class="center">
        <div class="state">
          <img v-if="level.status === 'completed'" src="../../assets/CodeBubbyAssets/20_13/5.svg" alt="完成" class="status-icon" />
          <img v-else-if="level.status === 'available'" src="../../assets/CodeBubbyAssets/20_13/17.svg" alt="可用" class="status-icon" />
          <img v-else-if="level.status === 'locked'" src="../../assets/CodeBubbyAssets/20_13/29.svg" alt="锁定" class="status-icon" />
          <span v-else-if="level.status === 'coming-soon'" class="coming-soon-text">敬请期待</span>
        </div>
        <StarRating v-if="level.status !== 'coming-soon'" :value="level.stars" :disable="level.status === 'locked'"/>
      </div>
    </div>
    
    <div v-if="selected" class="active-overlay"></div>
  </button>
</template>

<script setup>
import StarRating from './StarRating.vue';
import { computed } from 'vue';

const props = defineProps({
  level: { type: Object, required: true },
  selected: { type: Boolean, default: false }
});

const difficultyClass = computed(() => {
  switch(props.level.difficulty) {
    case '简单': return 'easy';
    case '中等': return 'medium';
    case '困难': return 'hard';
    default: return 'unknown';
  }
});

defineEmits(['select', 'mouseover', 'mouseleave']);
</script>

<style scoped>
.card {
  position: relative;
  width: 100%;
  height: var(--card-height);
  border-radius: var(--border-radius-medium);
  background: var(--gradient-card-normal);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card-normal);
  color: var(--color-text-primary);
  text-align: left;
  overflow: hidden;
  transition: transform .3s ease, box-shadow .3s ease, background .3s ease;
  outline: 1px solid var(--color-border);
  outline-offset: -1px;
  cursor: pointer;
}

.card:hover:not(.locked):not(.coming-soon) {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4);
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}

.card.locked {
  background: var(--gradient-card-locked);
  box-shadow: var(--shadow-card-locked);
  outline: 1px solid rgba(55, 65, 81, 0.5);
  cursor: not-allowed;
}

.card.coming-soon {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.7));
  box-shadow: var(--shadow-card-locked);
  outline: 1px solid rgba(55, 65, 81, 0.5);
  cursor: not-allowed;
  opacity: 0.8;
}

.coming-soon-text {
  color: #94a3b8;
  font-size: 16px;
  font-weight: 700;
}

.card.active {
  outline: 1px solid rgba(99, 102, 241, 0.5);
}

.card-content {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 17px;
  box-sizing: border-box;
  z-index: 2;
}

.active-overlay {
  position: absolute;
  inset: 1px;
  background: var(--gradient-card-active);
  backdrop-filter: blur(12px);
  opacity: 0.3;
  z-index: 1;
  pointer-events: none;
}

.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.index {
  font-weight: 700;
  font-size: 24px;
  color: #ffffff; /* 浅色字体 */
}

.card.locked .index {
  color: #6B7280;
}

.chip {
  font-size: 12px;
  padding: 5px 8px;
  border-radius: var(--border-radius-full);
  background: rgba(255, 255, 255, 0.1);
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

.chip.unknown {
  background: var(--color-unknown-bg);
  color: var(--color-unknown-text);
}

.center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
}

.status-icon {
  width: 24px;
  height: 24px;
}
</style>
