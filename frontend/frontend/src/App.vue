<script>
import TitleBar from '@/components/TitleBar.vue'
import BreadcrumbBar from '@/components/BreadcrumbBar.vue'
export default {
  components: {
    TitleBar,
    BreadcrumbBar
  }
}
</script>

<template>
  <v-card>
    <TitleBar />
  </v-card>
  <router-view/>
</template>

