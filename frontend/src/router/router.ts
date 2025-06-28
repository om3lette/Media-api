import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("../views/HomeView.vue")
    },
    {
      path: "/process/",
      name: "Process",
      component: () => import("../views/ProcessView.vue")
    },
    {
      path: "/:catchAll(.*)",
      redirect: "/"
    }
  ]
});

export default router;
