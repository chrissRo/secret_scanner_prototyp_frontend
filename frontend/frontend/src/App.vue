<script>
import TitleBar from '@/components/TitleBar.vue'
export default {

  components: {
    TitleBar,
  },
  computed: {
    showTitleBar() {
      const hideTitleBar = ['Login', 'NotFoundView']
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

