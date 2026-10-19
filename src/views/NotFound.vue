<template>
  <el-card class="box-card">
    <el-alert title="404 页面不存在" type="error"></el-alert>
    <el-button type="primary" @click="$router.push({ name: 'Home' })" style="margin-top: 15px">返回首页</el-button>
  </el-card>
</template>
<script setup></script>
<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
</style>
