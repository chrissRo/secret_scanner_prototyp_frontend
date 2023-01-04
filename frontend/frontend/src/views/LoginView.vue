<script>
export default {
  data() {
    return {
      form: false,
      username: '',
      password: '',
      loginForm: 'login-form'
    }
  },
  methods: {
    login() {
      console.log('Login ->' + this.username + ':' + this.password)
    }
  }
}
</script>

<template>
    <v-card width="30em" :class="loginForm">
      <v-form v-model="form" @submit.prevent="login">
        <v-row>
          <v-col>
            <v-text-field
              v-model="username"
              label="Username"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="password"
              label="Password"
              required
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col style="text-align: center">
            <v-btn color="primary" @click="login()">Login</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
</template>



<style>
.login-form {
  left      : 50%;
  top       : 50%;
  position  : absolute;
  transform : translate(-50%, -50%);
  padding: 1em;
}

</style>
