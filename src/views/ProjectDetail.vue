<template>
  <el-card class="box-card" v-if="currProj">
    <template #header>
      <span>项目详情</span>
    </template>
    <p><strong>项目名称：</strong>{{ currProj.name }}</p>
    <p><strong>简短描述：</strong>{{ currProj.shortDesc }}</p>
    <p><strong>技术栈：</strong>{{ currProj.shortTech }}</p>
    <p><strong>完整描述：</strong>{{ currProj.fullDesc }}</p>
    <p><strong>完整技术：</strong>{{ currProj.fullTech }}</p>
    <div style="margin-top: 16px; display: flex; gap: 10px">
      <el-button type="primary" @click="goList">返回项目列表(replace)</el-button>
      <el-button @click="goBack">返回上一页(go-1)</el-button>
    </div>
  </el-card>

  <el-alert title="项目ID无效，找不到该项目" type="error" v-else class="box-card"></el-alert>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const router = useRouter();

const projectList = [
  {
    id: 1,
    name: "Vue个人信息页面",
    shortDesc: "个人信息管理页面",
    shortTech: "Vue3、HTML、CSS",
    fullDesc:
      "基于Vue3实现个人信息展示与编辑，支持技能关键词搜索筛选，个人简介可展开与收起。页面采用组件化开发，模块划分清晰。",
    fullTech: "Vue3组合式API、v-model双向绑定、v-for列表渲染、computed计算属性"
  },
  {
    id: 2,
    name: "短视频剪辑作品",
    shortDesc: "短视频剪辑制作",
    shortTech: "PR、剪映",
    fullDesc: "使用PR完成短视频素材剪辑，画面裁剪、音频调节，添加字幕、转场特效。",
    fullTech: "Adobe Premiere、剪映专业版"
  }
];

const currProj = computed(() => {
  const id = Number(route.params.id);
  return projectList.find((p) => p.id === id);
});

const goList = () => {
  router.replace({ name: "ProjectList" });
};
const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
</style>
