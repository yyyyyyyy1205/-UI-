<template>
  <div class="module normal-module">
    <div class="part-title">个人项目展示区域</div>
    <BaseCard v-for="proj in projectList" :key="proj.id">
      <template #header>
        <h3>{{ proj.name }}</h3>
      </template>
      <template #default>
        <p>项目描述：{{ proj.shortDesc }}</p>
        <p>技术栈：{{ proj.shortTech }}</p>
      </template>
      <template #footer>
        <button @click="openDetail(proj)">查看详情</button>
        <button @click="openSourceCode(proj)">查看源码</button>
      </template>
    </BaseCard>

    <Teleport to="body">
      <div v-if="showDetailModal" class="modal-mask" @click="closeDetailModal">
        <div class="modal-box" @click.stop>
          <div class="modal-header">
            <h3>{{ currentProject.name }}</h3>
            <button class="close-btn" @click="closeDetailModal">×</button>
          </div>
          <div class="modal-body">
            <p><strong>项目描述：</strong>{{ currentProject.fullDesc }}</p>
            <p><strong>使用技术：</strong>{{ currentProject.fullTech }}</p>
          </div>
          <div class="modal-footer">
            <button @click="closeDetailModal">关闭</button>
          </div>
        </div>
      </div>

      <div v-if="showSourceModal" class="modal-mask" @click="closeSourceModal">
        <div class="modal-box source-modal" @click.stop>
          <div class="modal-header">
            <h3>{{ sourceProject.name }} - 源码片段</h3>
            <button class="close-btn" @click="closeSourceModal">×</button>
          </div>
          <div class="modal-body">
            <pre>{{ sourceProject.code }}</pre>
          </div>
          <div class="modal-footer">
            <button @click="closeSourceModal">关闭</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from "vue";
import BaseCard from "./BaseCard.vue";

defineProps({
  isDark: {
    type: Boolean,
    default: false
  }
});

const projectList = [
  {
    id: 1,
    name: "Vue个人信息页面",
    shortDesc: "个人信息管理页面",
    shortTech: "Vue3、HTML、CSS",
    fullDesc:
      "基于Vue3实现个人信息展示与编辑，支持技能关键词搜索筛选，个人简介可展开与收起。页面采用组件化开发，模块划分清晰，实现双向绑定、条件渲染等Vue基础功能，页面风格为天蓝色主题。",
    fullTech: "Vue3组合式API、v‑model双向绑定、v‑for列表渲染、v‑if/v‑show条件渲染、计算属性computed，原生HTML+CSS",
    code: "&lt;template&gt;\n  &lt;div class=\"info-module\"&gt;\n    &lt;p&gt;姓名：{{ info.name }}&lt;/p&gt;\n    &lt;p&gt;学号：{{ info.stuId }}&lt;/p&gt;\n    &lt;button @click=\"isEdit=true\"&gt;编辑&lt;/button&gt;\n  &lt;/div&gt;\n&lt;/template&gt;\n&lt;script setup&gt;\nimport {ref} from 'vue'\nconst info = ref({\n  name:'张三',\n  stuId:'2023001001'\n})\n&lt;/script&gt;"
  },
  {
    id: 2,
    name: "短视频剪辑作品",
    shortDesc: "短视频剪辑制作",
    shortTech: "PR、剪映",
    fullDesc:
      "使用PR完成短视频素材剪辑，进行画面裁剪、音频调节，添加字幕、转场特效，优化视频节奏；剪映辅助快速调色，完成成片输出。",
    fullTech: "Adobe Premiere、剪映专业版，掌握剪辑、字幕、音频处理、转场特效等多媒体制作技术",
    code: "该项目为视频剪辑项目，无程序源码。"
  }
];

const showDetailModal = ref(false);
const currentProject = ref({});
const openDetail = (proj) => {
  currentProject.value = proj;
  showDetailModal.value = true;
};
const closeDetailModal = () => {
  showDetailModal.value = false;
};

const showSourceModal = ref(false);
const sourceProject = ref({});
const openSourceCode = (proj) => {
  sourceProject.value = proj;
  showSourceModal.value = true;
};
const closeSourceModal = () => {
  showSourceModal.value = false;
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--mask-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal-box {
  width: 440px;
  background-color: var(--page-bg);
  border-radius: 10px;
  border: 2px solid var(--border-color);
  overflow: hidden;
  color: var(--text-normal);
}
.source-modal {
  width: 600px;
}
.modal-header {
  background-color: var(--btn-bg);
  color: #ffffff;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-btn {
  background: none;
  color: #ffffff;
  font-size: 22px;
  border: none;
  cursor: pointer;
  padding: 0 6px;
}
.modal-body {
  padding: 20px 18px;
  line-height: 1.8;
  color: var(--text-normal);
  font-size: 15px;
}
.modal-body pre {
  white-space: pre-wrap;
  background: var(--body-bg);
  color: var(--text-normal);
  padding: 10px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}
.modal-footer {
  text-align: center;
  padding: 12px;
  border-top: 1px solid var(--border-color);
}
</style>
