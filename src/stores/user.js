import { defineStore } from "pinia";
export const useUserStore = defineStore("user", {
  state() {
    return {
      intro:
        "我是计算机专业学生，学习Vue3前端开发。项目使用Element Plus、Vue Router和Pinia，实现路由跳转、文章增删改查和个人简介修改功能。"
    };
  },
  actions: {
    setIntro(val) {
      this.intro = val;
    }
  }
});
