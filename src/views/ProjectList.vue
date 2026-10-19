<template>
  <el-card class="box-card">
    <template #header>
      <span>项目列表</span>
    </template>
    <div class="item-wrap">
      <div class="item" v-for="project in projectList" :key="project.id">
        <h3>{{ project.name }}</h3>
        <p>{{ project.desc }}</p>
        <el-button type="primary" @click="$router.push({ name: 'ProjectDetail', params: { id: project.id } })"
          >查看详情</el-button
        >
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from "vue";
const projectList = ref([
  { id: 1, name: "个人主页", desc: "Vue个人展示主页项目" },
  { id: 2, name: "文章管理", desc: "Pinia管理文章数据" }
]);
</script>

<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
.item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
</style>
