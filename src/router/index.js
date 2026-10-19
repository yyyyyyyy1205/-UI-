import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Login from "../views/Login.vue";
import ProjectLayout from "../views/ProjectLayout.vue";
import ProjectList from "../views/ProjectList.vue";
import ProjectDetail from "../views/ProjectDetail.vue";
import AdminLayout from "../views/AdminLayout.vue";
import AdminProfile from "../views/AdminProfile.vue";
import ArticleList from "../views/ArticleList.vue";
import ArticleManage from "../views/ArticleManage.vue";
import NotFound from "../views/NotFound.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", name: "Home", component: Home, meta: { title: "个人主页-首页" } },
  { path: "/about", name: "About", component: About, meta: { title: "关于我" } },
  { path: "/login", name: "Login", component: Login, meta: { title: "登录页面" } },
  { path: "/article-list", name: "ArticleList", component: ArticleList, meta: { title: "文章列表" } },
  {
    path: "/admin",
    component: AdminLayout,
    children: [
      { path: "", name: "Admin", component: AdminProfile, meta: { title: "后台管理", requiresAuth: true } },
      {
        path: "profile",
        name: "AdminProfile",
        component: AdminProfile,
        meta: { title: "编辑资料", requiresAuth: true }
      },
      {
        path: "article-manage",
        name: "ArticleManage",
        component: ArticleManage,
        meta: { title: "文章管理", requiresAuth: true }
      }
    ]
  },
  {
    path: "/project",
    component: ProjectLayout,
    children: [
      { path: "", name: "ProjectList", component: ProjectList, meta: { title: "项目中心" } },
      { path: "detail/:id", name: "ProjectDetail", component: ProjectDetail, meta: { title: "项目详情" } }
    ]
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { title: "404页面不存在" }
  }
];

const router = createRouter({
  // ✅ 修改为 hash模式，适配GitHub Pages
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || "个人主页系统";
  const { useUserStore } = await import("../stores/useUserStore");
  const userStore = useUserStore();
  if (to.meta.requiresAuth) {
    if (userStore.isLogin) {
      next();
    } else {
      next({ name: "Login", query: { redirect: to.fullPath } });
    }
  } else {
    next();
  }
});

export default router;
