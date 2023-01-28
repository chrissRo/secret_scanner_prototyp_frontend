<script>
import {useTokenStore} from "@/store/token";

export default {
  setup() {
    return {
      tokenStore: useTokenStore()
    }
  },
  async created() {
    await this.getAvailableScanner()
  },
  data () {
      return {
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
        availableScanner: {}
      }
    },
  methods: {
      async uploadFindings() {
        console.log('Todo Upload')
        this.dialog = false
      },
      async getAvailableScanner() {
        this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
        this.$axios.get('/misc/scanner').then((res) =>{
          this.availableScanner = res.data
        }).catch((err)=>{
          // Todo
          console.log(err)
        })
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
        <v-list-item title="Repository Information"></v-list-item>
        <v-list-item>
          <v-row>
            <v-col>
              <v-text-field
                label="Repository Name*"
                required
              ></v-text-field>
            </v-col>
          <v-col>
            <v-text-field
              label="Repository Path/Address*"
              required
            ></v-text-field>
          </v-col>
          </v-row>
        </v-list-item>
        <v-list-item>
          <v-row>
            <v-col>
              <v-select
                :items="Object.keys(this.availableScanner)"
                label="Scanner Type*"
                required
              ></v-select>
            </v-col>
            <v-col>
              <v-text-field
                label="Scanner Version*"
                required
              ></v-text-field>
            </v-col>
          </v-row>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list>
        <v-list-item title="Data"></v-list-item>
        <v-list-item>todo -> Drag and Drop?</v-list-item>
      </v-list>
    </v-card>
  </v-dialog>
</template>
