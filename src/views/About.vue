<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>👤关于我</span>
      </div>
    </template>
    <p>姓名：杨美媛 | 班级：24计科2班</p>
    <el-tag type="success">Vue前端开发</el-tag>
    <el-tag type="info">组件化开发</el-tag>
    <el-tag type="warning">视频剪辑</el-tag>

    <h3 style="margin: 20px 0 10px">学习经历时间线</h3>
    <el-timeline>
      <el-timeline-item timestamp="2025‑09" placement="top">学习HTML、CSS基础网页开发</el-timeline-item>
      <el-timeline-item timestamp="2026‑03" placement="top">学习Vue3组合式API与组件开发</el-timeline-item>
      <el-timeline-item timestamp="2026‑09" placement="top">学习Vue‑Router路由与Pinia状态管理</el-timeline-item>
    </el-timeline>
  </el-card>
</template>
<script setup></script>
<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style>
