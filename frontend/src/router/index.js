import Vue from "vue";
import VueRouter from "vue-router";
import ChatRoom from "@/components/ChatRoom.vue";
import ChatRoomList from "@/components/ChatRoomList.vue";
import LoginPage from "@/components/LoginPage.vue";
import RegisterPage from "@/components/RegisterPage.vue";
import UserList from "@/components/UserList.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "/loginPage",
  },
  {
    path: "/loginPage",
    component: LoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: "/registerPage",
    component: RegisterPage,
    meta: { requiresAuth: false },
  },
  {
    path: "/chatRoomList",
    component: ChatRoomList,
    meta: { requiresAuth: true },
  },
  {
    path: "/userList",
    component: UserList,
    meta: { requiresAuth: true },
  },
  {
    path: "/chatRoom/:id",
    name: "ChatRoom",
    component: ChatRoom,
    props: true,
    meta: { requiresAuth: true },
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  const access = localStorage.getItem("access");
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!access) {
      next({ path: "/loginPage" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
