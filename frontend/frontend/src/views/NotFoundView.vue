<script>
export default {
  data() {
    return {
      notFoundContainer: 'not-found-container'
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<template>
  <v-card width="30em" :class="notFoundContainer">
      <v-row>
        <v-col style="text-align: center;">
          <h2>Page not Found 404</h2>
        </v-col>
       </v-row>
      <v-row>
        <v-col style="text-align: center">
          <v-btn color="primary" @click="goToLogin()" >Back To Login</v-btn>
        </v-col>
      </v-row>
  </v-card>
</template>

<style>
.not-found-container {
  left      : 50%;
  top       : 50%;
  position  : absolute;
  transform : translate(-50%, -50%);
  padding: 1em;
}
</style>
