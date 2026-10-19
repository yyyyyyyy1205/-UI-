<template>
  <div>
    <h4>编辑个人简介</h4>
    <el-textarea v-model="desc" :rows="6" placeholder="请输入个人简介"></el-textarea>
    <el-button type="primary" @click="save" style="margin-top: 10px">保存修改</el-button>
  </div>
</template>

<script setup>
import { ref } from "vue";
const desc = ref("");
const save = () => {
  alert("保存成功！");
};
</script>
