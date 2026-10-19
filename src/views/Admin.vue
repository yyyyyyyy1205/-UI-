<template>
  <el-card>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="编辑个人资料" name="info">
        <h3>编辑个人简介</h3>
        <el-input
          v-model="localIntro"
          type="textarea"
          :rows="4"
          placeholder="输入个人简介"
          style="width: 100%; margin: 10px 0"
        ></el-input>
        <el-button type="primary" @click="saveIntro">保存修改</el-button>
      </el-tab-pane>

      <el-tab-pane label="文章管理" name="article">
        <el-button type="primary" @click="openAddDialog">新增文章</el-button>
        <h4>已有文章列表</h4>
        <div v-for="(item, index) in articleStore.articles" :key="index" style="margin: 16px 0">
          <h4>{{ item.title }}</h4>
          <p>{{ item.content }}</p>
          <el-button size="small" @click="openEditDialog(item)">编辑</el-button>
          <el-button size="small" type="danger" @click="delArticle(index)">删除</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="articleDialog.visible" title="编辑文章">
      <el-form>
        <el-form-item label="标题">
          <el-input v-model="articleForm.title"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="articleForm.content" type="textarea" :rows="4"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="articleDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveArticle">确定保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted, reactive, nextTick } from "vue";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/user";
import { useArticleStore } from "@/stores/article";

const activeTab = ref("info");
const userStore = useUserStore();
const articleStore = useArticleStore();
const localIntro = ref("");

onMounted(() => {
  localIntro.value = userStore.intro;
});
function saveIntro() {
  userStore.setIntro(localIntro.value);
  ElMessage.success("个人简介保存成功！");
}

const articleDialog = ref({
  visible: false,
  isEdit: false
});
// =========重点！这里改成 reactive！！！============
const articleForm = reactive({
  title: "",
  content: ""
});

function openAddDialog() {
  articleDialog.value.visible = true;
  articleDialog.value.isEdit = false;
  articleForm.title = "";
  articleForm.content = "";
}

function openEditDialog(item) {
  articleDialog.value.visible = true;
  articleDialog.value.isEdit = true;
  articleForm.title = item.title;
  articleForm.content = item.content;
}

function saveArticle() {
  if (articleDialog.value.isEdit) {
    articleStore.editArticle(articleForm);
  } else {
    articleStore.addArticle({ ...articleForm });
  }
  articleDialog.value.visible = false;
  ElMessage.success("文章保存成功");
}

function delArticle(index) {
  articleStore.deleteArticle(index);
  ElMessage.success("已删除文章");
}
</script>

<style scoped>
.el-card {
  max-width: 900px;
  margin: 20px auto;
}
</style>
