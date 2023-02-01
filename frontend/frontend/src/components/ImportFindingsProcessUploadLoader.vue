<script>
export default {
  props: {
    propsDialog: null,
    propsStepCounter: null
  },
  data () {
    return {
      dialog: this.propsDialog,
    }
  },
}
</script>


<template>
  <div class="text-center">
    <v-dialog
      v-model="this.dialog"
      :scrim="false"
      persistent
    >
      <v-card
        color="primary"
      >
        <v-card-text>
          Uploading please wait
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<style>

</style>

