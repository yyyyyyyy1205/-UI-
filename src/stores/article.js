import { defineStore } from "pinia";
export const useArticleStore = defineStore("article", {
  state() {
    return {
      articles: [
        { title: "Vue3学习笔记", content: "学习组合式API、props、emit、插槽等组件知识。" },
        { title: "Vue-Router学习", content: "学习动态路由、嵌套路由、路由守卫实现单页面应用。" }
      ]
    };
  },
  actions: {
    addArticle(data) {
      this.articles.push(data);
    },
    editArticle(data) {
      const idx = this.articles.findIndex((a) => a.title === data.title);
      if (idx !== -1) this.articles[idx].content = data.content;
    },
    deleteArticle(index) {
      this.articles.splice(index, 1);
    }
  }
});
