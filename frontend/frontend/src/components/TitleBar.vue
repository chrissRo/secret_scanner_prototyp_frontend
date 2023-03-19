<script>
import {useTokenStore} from "@/store/token";
import ToolbarMenuDropdown from "@/components/ToolbarMenuDropdown";

export default {
  components: {ToolbarMenuDropdown},
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
      localStorage.removeItem(this.tokenStore.token)
      this.tokenStore.token = null
      this.$router.push('/login')
    }
  }
}
</script>


<template>
      <v-toolbar border>
        <v-btn @click="$router.back()"><v-icon x-large>mdi-arrow-left-circle</v-icon></v-btn>
        <router-link :to="{name: 'HomeView'}" scope="v-btn" style="text-decoration: none;">
          <v-btn color="primary">
            <v-icon x-large>mdi-home</v-icon>
          </v-btn>
        </router-link>
        <v-toolbar-title>Welcome to Gitleaks Review Frontend</v-toolbar-title>
        <v-spacer></v-spacer>
        <div :class="navigationButtonGroup">
          <ToolbarMenuDropdown/>
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
