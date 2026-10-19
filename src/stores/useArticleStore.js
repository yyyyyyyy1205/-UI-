import { defineStore } from "pinia";

export const useArticleStore = defineStore("article", {
  state: () => ({
    articleList: []
  }),
  getters: {
    getAllArticles: (state) => state.articleList
  },
  actions: {
    restoreArticle() {
      const str = localStorage.getItem("articleList");
      if (str) {
        this.articleList = JSON.parse(str);
      } else {
        this.articleList = [
          { id: 1, title: "Vue3学习笔记", content: "学习组合式API、props、emit、插槽等组件知识。" },
          { id: 2, title: "Vue‑Router学习", content: "学习动态路由、嵌套路由、路由守卫实现单页面应用。" }
        ];
        this.saveToLocal();
      }
    },
    saveToLocal() {
      localStorage.setItem("articleList", JSON.stringify(this.articleList));
    },
    addArticle(item) {
      const newId = Date.now();
      this.articleList.push({ id: newId, ...item });
      this.saveToLocal();
    },
    delArticle(id) {
      const index = this.articleList.findIndex((a) => a.id === id);
      if (index !== -1) {
        this.articleList.splice(index, 1);
        this.saveToLocal();
      }
    },
    getArticleById(id) {
      return this.articleList.find((a) => a.id === id);
    },
    updateArticle(editItem) {
      const idx = this.articleList.findIndex((a) => a.id === editItem.id);
      if (idx !== -1) {
        this.articleList[idx] = { ...editItem };
        this.saveToLocal();
      }
    }
  }
});
