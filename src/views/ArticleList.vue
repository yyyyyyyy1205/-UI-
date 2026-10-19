<template>
  <el-card class="box-card">
    <template #header>
      <span>文章列表</span>
    </template>
    <div v-for="item in articleList" :key="item.id" class="article-item">
      <h3>{{ item.title }}</h3>
      <p>{{ item.content }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { onMounted } from "vue";
import { useArticleStore } from "../stores/useArticleStore";
import { storeToRefs } from "pinia";

const articleStore = useArticleStore();
const { articleList } = storeToRefs(articleStore);

onMounted(() => {
  articleStore.restoreArticle();
});
</script>

<style scoped>
.box-card {
  max-width: 900px;
  margin: 20px auto;
}
.article-item {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}
</style>
