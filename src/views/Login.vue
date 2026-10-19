<template>
  <el-card class="box-card">
    <template #header>
      <span>🔐后台登录</span>
    </template>
    <p>模拟登录后台管理系统</p>
    <el-button type="primary" @click="doLogin">登录</el-button>
    <el-button @click="backHome">返回首页</el-button>
  </el-card>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "../stores/useUserStore";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const doLogin = () => {
  userStore.login();
  alert("登录成功！");
  const redirectPath = route.query.redirect || "/admin/profile";
  router.push(redirectPath);
};
const backHome = () => {
  router.push({ name: "Home" });
};
</script>

<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
</style>
