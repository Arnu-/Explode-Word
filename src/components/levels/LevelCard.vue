<template>
  <button
    class="card"
    :class="[{ 
      selected, 
      locked: level.status === 'locked',
      active: selected
    }]"
    @click="$emit('select', level)"
    :disabled="level.status === 'locked'"
  >
    <div class="card-content">
      <div class="top">
        <span class="index">{{ level.id }}</span>
        <span class="chip" :class="difficultyClass">{{ level.difficulty }}</span>
      </div>

      <div class="center">
        <div class="state">
          <img v-if="level.status === 'completed'" src="../../assets/CodeBubbyAssets/20_13/5.svg" alt="完成" class="status-icon" />
          <img v-else-if="level.status === 'available'" src="../../assets/CodeBubbyAssets/20_13/17.svg" alt="可用" class="status-icon" />
          <img v-else src="../../assets/CodeBubbyAssets/20_13/29.svg" alt="锁定" class="status-icon" />
        </div>
        <StarRating :value="level.stars" />
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

defineEmits(['select']);
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
  transition: transform .15s ease, box-shadow .2s ease;
  outline: 1px solid var(--color-border);
  outline-offset: -1px;
  cursor: pointer;
}

.card.locked {
  background: var(--gradient-card-locked);
  box-shadow: var(--shadow-card-locked);
  outline: 1px solid rgba(55, 65, 81, 0.5);
  cursor: not-allowed;
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
