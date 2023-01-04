<script>
import TitleBar from '@/components/TitleBar.vue'
import BreadcrumbBar from '@/components/BreadcrumbBar.vue'
export default {

  components: {
    TitleBar,
    BreadcrumbBar
  },
  computed: {
    showTitleBar() {
      const hideTitleBar = ['Login']
      return !hideTitleBar.includes(this.$route.name);
    }
  }
}
</script>

<template>
  <v-card v-if="showTitleBar">
    <TitleBar />
  </v-card>
  <router-view/>
</template>

