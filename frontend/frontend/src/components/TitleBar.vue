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
      navigationButtonGroup: 'navigation-button-group',
      navigationButton: 'navigation-button'
    }
  },
  methods: {
    logout() {
      this.tokenStore.signOut()
      this.$router.push('/login')
    }
  }
}
</script>


<template>
  <v-toolbar border>
    <v-btn @click="$router.back()"><v-icon x-large>mdi-arrow-left-circle</v-icon></v-btn>
  <v-toolbar-title>Welcome to FP-Marker</v-toolbar-title>
    <v-spacer></v-spacer>
    <div :class="navigationButtonGroup">
      <v-btn :class="navigationButton" variant="tonal" color="info">Todo: Import/Export</v-btn>
      <v-btn :class="navigationButton" variant="tonal" color="info">Repositories-View</v-btn>
      <v-btn :class="navigationButton" variant="tonal" color="info">Files-View</v-btn>
      <v-btn :class="navigationButton" variant="tonal" color="primary" @click="logout" >Logout</v-btn>
    </div>
  </v-toolbar>
</template>

<style>
.navigation-button-group {
  margin: 1em;
}

.navigation-button {
  margin: 0.5em;
}
</style>
