<template>
  <div>
    <h1>个人简介</h1>
    <div style="border: 1px solid #e4e7ed; border-radius: 8px; padding: 24px; max-width: 900px">
      <p>简介文字：{{ introText }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
const introText = ref(
  "我是计算机专业学生，学习Vue3前端开发。项目使用Element Plus、Vue Router和Pinia，实现路由跳转、文章增删改查和个人简介修改功能。"
);
</script>
