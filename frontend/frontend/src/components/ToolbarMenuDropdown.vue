<script>
import {useTokenStore} from "@/store/token";
import ImportFindings from "@/components/ImportFindings";

export default {
  components: {ImportFindings},
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
    <v-list density="compact" style="margin-top: 0.7em" >
      <v-list-item :class="listItem"><template v-slot:prepend><v-icon icon="mdi-database-import"></v-icon></template><ImportFindings/></v-list-item>
      <v-list-item :class="listItem"><template v-slot:prepend><v-icon icon="mdi-database-export"></v-icon></template><v-list-item-title>Export Findings</v-list-item-title></v-list-item>
      <v-divider></v-divider>
      <v-list-item :class="listItem">
        <template v-slot:prepend><v-icon icon="mdi-source-repository"></v-icon></template>
        <router-link :to="{name: 'HomeView'}"
                     v-slot="{navigate}"
                     style="text-decoration: none;">
        <v-list-item-title @click="navigate" style="color: black">Repositories</v-list-item-title>
        </router-link>
      </v-list-item>
      <v-list-item :class="listItem">
        <template v-slot:prepend><v-icon icon="mdi-star"></v-icon></template>
        <router-link :to="{name: 'FavouriteView'}"
                     v-slot="{navigate}"
                     style="text-decoration: none;">
          <v-list-item-title @click="navigate" style="color: black">Favourites</v-list-item-title>
        </router-link>
      </v-list-item>
      <v-list-item :class="listItem">
        <template v-slot:prepend><v-icon icon="mdi-check"></v-icon></template>
        <router-link :to="{name: 'TruePositiveView'}"
                     v-slot="{navigate}"
                     style="text-decoration: none;">
          <v-list-item-title @click="navigate" style="color: black">True Positives</v-list-item-title>
        </router-link>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item :class="listItem" @click="logout">
        <template v-slot:prepend><v-icon icon="mdi-logout"></v-icon></template>
        <v-list-item-title>Logout</v-list-item-title></v-list-item>
    </v-list>
  </v-menu>
</template>

<style>
.list-item:hover {
  background-color: aliceblue;
  cursor: pointer;
}

</style>
