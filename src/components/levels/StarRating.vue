<template>
  <div class="stars">
    <img v-for="i in 3" :key="i" 
         :src="getStarImage(i)" 
         :class="['star', { filled: i <= value }]" 
         alt="星星" />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  disable : { type: Boolean, default: false },
  value: { type: Number, default: 0 }, // 0..3
  size: { type: Number, default: 18 }
});

// 根据星星状态获取对应的图片
function getStarImage(index) {
  if(props.disable) {return '../../assets/CodeBubbyAssets/20_13/30.svg';}
  if (index <= props.value) {
    return '../../assets/CodeBubbyAssets/20_13/39.svg'; // 填充星星
  } else {
    return '../../assets/CodeBubbyAssets/20_13/31-light.svg'; // 空心星星
  }
}
</script>

<style scoped>
.stars { 
  display: inline-flex; 
  gap: 4px; 
}
.star { 
  width: 18px; 
  height: 16px; 
}
</style>
