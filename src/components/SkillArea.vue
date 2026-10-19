<template>
  <div class="module">
    <div class="part-title">个人技能与兴趣区域</div>
    <span class="skill" v-for="item in skillList" :key="item">{{ item }}</span>
  </div>
</template>
<script setup>
defineProps({
  skillList: {
    type: Array,
    required: true
  }
});
</script>
