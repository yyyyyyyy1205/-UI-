<template>
  <el-card class="box-card">
    <template #header>
      <span>🔧后台管理中心</span>
    </template>
    <el-menu mode="horizontal" :router="true">
      <el-menu-item index="/admin/profile">编辑个人资料</el-menu-item>
      <el-menu-item index="/admin/article-manage">文章管理</el-menu-item>
    </el-menu>
    <div style="margin-top: 16px">
      <RouterView />
    </div>
  </el-card>
</template>
<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
</style>
