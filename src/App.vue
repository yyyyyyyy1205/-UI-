<template>
  <el-container>
    <el-header height="70px">
      <el-menu mode="horizontal" :router="true" active-text-color="#409eff" background-color="#ecf5fc">
        <el-menu-item index="/home">首页</el-menu-item>
        <el-menu-item index="/about">关于我</el-menu-item>
        <el-menu-item index="/project">项目中心</el-menu-item>
        <el-menu-item index="/article-list">文章列表</el-menu-item>
        <el-menu-item index="/admin" v-if="userStore.isLogin">后台管理</el-menu-item>
        <el-menu-item index="/login" v-if="!userStore.isLogin">登录</el-menu-item>
        <template #append>
          <el-button v-if="userStore.isLogin" type="primary" @click="handleLogout">退出登录</el-button>
        </template>
      </el-menu>
    </el-header>
    <el-main>
      <RouterView />
    </el-main>
  </el-container>
</template>

<script setup>
import { onMounted } from "vue";
import { useUserStore } from "./stores/useUserStore";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { isLogin } = storeToRefs(userStore);

onMounted(() => {
  userStore.restoreLoginState();
});

const handleLogout = () => {
  userStore.logout();
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
.el-header {
  padding: 0;
}
</style>
