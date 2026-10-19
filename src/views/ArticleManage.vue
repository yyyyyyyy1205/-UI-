<template>
  <div>
    <el-button type="primary" @click="openAdd">新增文章</el-button>

    <el-dialog v-model="dialogVisible" :title="editId ? '编辑文章' : '新增文章'">
      <el-form :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-textarea v-model="form.content" :rows="5"></el-textarea>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定保存</el-button>
      </template>
    </el-dialog>

    <el-card style="margin-top: 20px">
      <template #header><span>已有文章列表</span></template>
      <!-- 删掉错误el-list，改用原生div -->
      <div class="article-wrap">
        <div class="article-item" v-for="art in articleList" :key="art.id">
          <h5>{{ art.title }}</h5>
          <p>{{ art.content }}</p>
          <el-button size="small" @click="openEdit(art)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDel(art.id)">删除</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useArticleStore } from "../stores/useArticleStore";
import { storeToRefs } from "pinia";

const articleStore = useArticleStore();
const { articleList } = storeToRefs(articleStore);

const dialogVisible = ref(false);
const editId = ref(null);
const form = ref({
  title: "",
  content: ""
});

onMounted(() => {
  articleStore.restoreArticle();
});

const openAdd = () => {
  editId.value = null;
  form.value = { title: "", content: "" };
  dialogVisible.value = true;
};

const openEdit = (artItem) => {
  editId.value = artItem.id;
  form.value.title = artItem.title;
  form.value.content = artItem.content;
  dialogVisible.value = true;
};

const submitForm = () => {
  if (!form.value.title || !form.value.content) {
    alert("标题和内容不能为空！");
    return;
  }
  if (editId.value) {
    articleStore.updateArticle({ id: editId.value, ...form.value });
  } else {
    articleStore.addArticle({ ...form.value });
  }
  dialogVisible.value = false;
  alert("操作成功");
};

const handleDel = (id) => {
  if (confirm("确定要删除该文章吗?")) {
    articleStore.delArticle(id);
    alert("删除完成");
  }
};
</script>

<style scoped>
.article-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}
</style>
