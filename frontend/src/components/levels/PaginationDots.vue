<template>
  <div class="pagination">
    <button class="nav-button prev" @click="$emit('prev')" :disabled="current <= 1">
      <img src="../../assets/CodeBubbyAssets/20_13/37.svg" alt="上一页" />
    </button>
    
    <button 
      v-for="i in total" 
      :key="i"
      class="page-button"
      :class="{ active: i === current }"
      @click="$emit('change', i)"
    >
      {{ i }}
    </button>
    
    <button class="nav-button next" @click="$emit('next')" :disabled="current >= total">
      <img src="../../assets/CodeBubbyAssets/20_13/38.svg" alt="下一页" />
    </button>
  </div>
</template>

<script setup>
defineProps({ 
  total: { type: Number, required: true }, 
  current: { type: Number, required: true }
});
defineEmits(['change', 'prev', 'next']);
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.nav-button, .page-button {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background: rgba(255, 255, 255, 0.1);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-primary);
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-button img {
  width: 10px;
  height: 16px;
}

.page-button.active {
  background: rgba(255, 255, 255, 0.3);
  font-weight: 700;
}

.page-button:not(.active) {
  font-weight: 400;
}

.page-button:hover:not(.active),
.nav-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}
</style>
