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
      listItem: 'list-item'
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
  <v-menu open-on-hover>
    <template v-slot:activator="{ props }">
      <v-btn
        color="primary"
        v-bind="props"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </template>
    <v-list density="compact" style="margin-top: 0.5em">
      <v-list-item :class="listItem"><v-list-item-title>Import Findings</v-list-item-title></v-list-item>
      <v-list-item :class="listItem"><v-list-item-title>Export Findings</v-list-item-title></v-list-item>
      <v-divider></v-divider>
      <v-list-item :class="listItem">
        <router-link :to="{name: 'HomeView'}"
                     v-slot="{navigate}"
                     style="text-decoration: none;">
        <v-list-item-title @click="navigate" >Repository Overview</v-list-item-title>
        </router-link>
      </v-list-item>
      <v-list-item :class="listItem">
        <router-link :to="{name: 'FavouriteView'}"
                     v-slot="{navigate}"
                     style="text-decoration: none;">
          <v-list-item-title @click="navigate" >Favourite Overview</v-list-item-title>
        </router-link>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item :class="listItem" @click="logout"><v-list-item-title>Logout</v-list-item-title></v-list-item>
    </v-list>
  </v-menu>
</template>

<style>
.list-item:hover {
  background-color: aliceblue;
}
</style>
