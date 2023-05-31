<template>
  <v-app>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="8">
        <v-card class="elevation-12">
          <!--          <v-row>-->
          <!--            <v-col>-->
          <!--                <v-text-field></v-text-field>-->
          <!--            </v-col>-->
          <v-col cols="12" md="8">
            <v-card-text class="mt-12">
              <v-form>
                <v-text-field
                  label="Username"
                  name="Username"
                  prepend-icon="mdi-account"
                  type="text"
                  v-model="username"
                  required
                  color="#2C3A47"
                />
                <v-text-field
                  label="Password"
                  name="Password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="password"
                  required
                  color="#2C3A47"
                  @keyup.enter="loginAndClose"
                />
              </v-form>
            </v-card-text>
            <div class="text-center mt-3">
              <v-btn
                rounded
                color="#2C3A47"
                dark
                outlined
                @click="loginAndClose"
                @submit.prevent="loginAndClose"
              >
                Login
              </v-btn>

              <span class="mx-3"></span>

              <v-btn
                rounded
                color="#2C3A47"
                dark
                outlined
                @click="goToRegister"
                @submit.prevent="goToRegister"
              >
                Save
              </v-btn>

              <v-alert
                v-if="error"
                outlined
                type="error"
                class="mt-3"
                dismissible
              >
                {{ error }}
              </v-alert>
            </div>
          </v-col>
        </v-card>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch("api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });
        if (response.status === 401) {
          this.error = "Invalid username or password.";
          this.username = "";
          this.password = "";
        } else if (!response.ok) {
          throw new Error(response.json().toString());
        } else {
          const data = await response.json();
          window.localStorage.setItem("username", this.username);
          window.localStorage.setItem("access", data.access);
          this.$emit("success");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async loginAndClose() {
      await this.login();
      if (!this.error) {
        await this.$router.push("/chatRoomList");
        location.reload();
      }
    },
    goToRegister() {
      this.$router.push("/registerPage");
    },
  },
};
</script>
