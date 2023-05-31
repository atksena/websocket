import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "@/router";
// import VueNativeSock from "vue-native-websocket";

// Vue.use(VueNativeSock, "ws://" + host + "/api/rooms/", {
//   reconnection: true,
//   reconnectionAttempts: 5,
//   reconnectionDelay: 3000,
// });

Vue.config.productionTip = false;

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
