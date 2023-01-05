<script>
import {useTokenStore} from "@/store/token";

export default {
  setup() {
    return {
      tokenStore: useTokenStore()
    }
  },
  data() {
    return {
      showPassword: false,
      form: false,
      username: '',
      password: '',
      loginForm: 'login-form',
      loginFailed: false,
      snackbarTimeout: 1000,
    }
  },
  methods: {
    async login() {
      console.log('Login ->' + this.username + ':' + this.password)
      // Todo api-call for login
      let formData = new FormData()
      formData.append('username', this.username)
      formData.append('password', this.password)

      let config = {
        headers: {
          'Access-Control-Allow-Origin': '*'
        }
      }

      this.$axios.post('/token/', formData, config).then((r) => {
        console.log(r)
        console.log('Token -> ' + this.tokenStore.token)
        if(this.tokenStore.token) {
          this.loginFailed = false
          this.$router.push('/')
        } else {
          this.loginFailed = true
        }
      }).catch((e) => {
        console.log(e.toString())
      })
    }
  },
  computed: {
    disableLoginButton() {
      return this.username === '' || this.password === '';
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
              label="Username*"
              required
              append-icon="mdi-account-outline"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="password"
              label="Password*"
              required
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col style="text-align: center">
            <v-btn v-if="disableLoginButton" color="primary" disabled>Login</v-btn>
            <v-btn v-else color="primary" @click="login()" >Login</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-snackbar v-model="loginFailed" :timeout="snackbarTimeout" rounded="pill" color="primary">
            Username or Password incorred. Please try again <v-icon>mdi-alert-circle</v-icon>
          </v-snackbar>
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
