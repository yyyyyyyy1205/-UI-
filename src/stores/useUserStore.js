import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    isLogin: false
  }),
  getters: {
    isUserLogin: (state) => state.isLogin
  },
  actions: {
    login() {
      this.isLogin = true;
      localStorage.setItem("isLogin", "true");
    },
    logout() {
      this.isLogin = false;
      localStorage.removeItem("isLogin");
    },
    restoreLoginState() {
      const storage = localStorage.getItem("isLogin");
      this.isLogin = storage === "true";
    }
  }
});
