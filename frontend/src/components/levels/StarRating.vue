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

// 导入星星图片
import disabledStar from '@/assets/CodeBubbyAssets/20_13/30.svg';
import filledStar from '@/assets/CodeBubbyAssets/20_13/39.svg';
import emptyStar from '@/assets/CodeBubbyAssets/20_13/31-light.svg';

const props = defineProps({
  disable : { type: Boolean, default: false },
  value: { type: Number, default: 0 }, // 0..3
  size: { type: Number, default: 18 }
});

// 根据星星状态获取对应的图片
function getStarImage(index) {
  if(props.disable) {
    return disabledStar;
  }
  if (index <= props.value) {
    return filledStar; // 填充星星
  } else {
    return emptyStar; // 空心星星
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
