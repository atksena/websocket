<template>
  <v-app>
    <v-main>
      <v-container>
        <v-app-bar app color="grey darken-3" dense dark>
          <v-layout align-center>
            <v-flex>
              <span class="title">CHAT</span>
            </v-flex>
            <v-flex shrink>
              <span>{{ username }}</span>
            </v-flex>
          </v-layout>
        </v-app-bar>
        <v-card>
          <v-card-text>
            <v-list>
              <span>Users</span>
              <v-list-item v-for="user in users" :key="user">
                <v-list-item-content>
                  <v-list-item-title>{{ user }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "UserList",
  data() {
    return {
      users: [],
      username: window.localStorage.getItem("username"),
    };
  },
  mounted() {
    const localStorageUsers = JSON.parse(localStorage.getItem("users"));
    if (localStorageUsers) {
      this.users = localStorageUsers;
    }
  },
};
</script>
