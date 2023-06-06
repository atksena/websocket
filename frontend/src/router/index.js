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
    component: LoginPage,
  },
  {
    path: "/loginPage",
    component: LoginPage,
  },
  {
    path: "/chatRoomList",
    component: ChatRoomList,
  },
  {
    path: "/userList",
    component: UserList,
  },
  {
    path: "/registerPage",
    component: RegisterPage,
  },
  {
    path: "/chatRoom/:id",
    name: "ChatRoom",
    component: ChatRoom,
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  const access = localStorage.getItem("access");
  if (to.path !== "/" && (access === null || access === undefined)) {
    if (to.path !== "/loginPage") {
      next({ path: "/loginPage" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
