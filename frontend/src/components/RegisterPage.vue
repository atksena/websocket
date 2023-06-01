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
                <p v-if="error" class="error">{{ error }}</p>
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
    register() {
      // eslint-disable-next-line no-async-promise-executor
      return new Promise(async (resolve, reject) => {
        try {
          if (this.password !== this.confirmPassword) {
            this.password = "";
            this.confirmPassword = "";
            return reject("Passwords do not match");
          }
          const response = await fetch("http://localhost/api/register/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
              confirm_password: this.confirmPassword,
            }),
          });
          if (response.status === 400) {
            this.error = "Registration failed";
            return reject("Registration failed");
          } else {
            const data = await response.json();
            window.localStorage.setItem("username", this.username);
            window.localStorage.setItem("access", data.access);
            resolve();
          }
        } catch (error) {
          console.error(error);
          reject(error);
        }
      });
    },
    async registerAndClose() {
      try {
        await this.register();
        if (!this.error) {
          await this.$router.push("/loginPage");
          location.reload();
        }
        console.log("Registration successful");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
