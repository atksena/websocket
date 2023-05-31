<template>
  <v-app>
    <v-row align="center" justify="center">
      <v-col cols="8" sm="6" md="6">
        <v-card class="elevation-12">
          <v-col cols="12" md="8">
            <v-card-text class="mt-12">
              <v-form @submit.prevent="registerAndClose">
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
                />
                <v-text-field
                  label="Confirm Password"
                  name="ConfirmPassword"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="confirmPassword"
                  required
                  color="#2C3A47"
                  @keyup.enter="registerAndClose"
                />
                <v-btn rounded color="#2C3A47" dark outlined type="submit">
                  Save
                </v-btn>
              </v-form>
            </v-card-text>
          </v-col>
        </v-card>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "RegisterPage",
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      error: null,
    };
  },
  methods: {
    async register() {
      try {
        if (this.password !== this.confirmPassword) {
          this.password = "";
          this.confirmPassword = "";
          return;
        }
        const response = await fetch("api/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            confirmPassword: this.confirmPassword,
          }),
        });
        if (response.status == 400) {
          this.username = "";
          this.password = "";
          this.confirmPassword = "";
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
    async registerAndClose() {
      await this.register();
      // if (!this.error) {
      //   await this.$router.push("/loginPage");
      //   location.reload();
      // }
    },
  },
};
</script>
