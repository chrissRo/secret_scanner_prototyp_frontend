<script>
export default {
    data () {
      return {
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
      }
    },
  methods: {
      async uploadFindings() {
        console.log('Todo Upload')
        this.dialog = false
      }
  }
  }
</script>

<template>
  <v-dialog
    v-model="dialog"
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition"
  >
    <template v-slot:activator="{ props }">
      <div v-bind="props">Import Findings</div>
    </template>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="dialog = false"><v-icon>mdi-close</v-icon></v-btn>
        <v-toolbar-title>Import Findings</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn variant="text" @click="uploadFindings()">Upload</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-list lines="two" subheader>
        <v-list-subheader>Data </v-list-subheader>
      </v-list>
      <v-divider></v-divider>
    </v-card>
  </v-dialog>
</template>
