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
        importDialog: false,
        availableScanner: {},
        repositoryInformation: {
          repositoryName: '',
          repositoryPath: '',
          scannerType: '',
          scannerVersion: '',
          scanDate: Date},
        repositoryInformationUpload: {},
        fileUploadRules: [
          value => {
            return !value || !value.length || value[0].size < 10000000 || 'File size should be less than 10 MB!'
          },
        ],
        findingFile: null,
        findingFiles: [],
        cancelImport: false,
        uploadDialog: false,
        uploadStepCounter: 0
      }
    },
  methods: {
      async uploadFindings() {
        this.findingFiles.forEach((f) =>{
          this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
          let formData = new FormData()
          formData.append('scannerType',this.availableScanner[this.repositoryInformationUpload.scannerType])
          formData.append('scannerVersion',this.repositoryInformationUpload.scannerVersion)
          formData.append('inputType', 1)
          formData.append('repositoryPath',this.repositoryInformationUpload.repositoryPath)
          formData.append('repositoryName',this.repositoryInformationUpload.repositoryName)
          formData.append('scanDate', '2023-01-31 18:46:45.156038')
          formData.append('new_file', new Blob(f))
          //this.uploadStepCounter += 1
          this.$axios.post(
            '/finding/file_upload',
            formData,
            { headers: {'Content-Type': 'multipart/form-data'}}
          ).then((res) => {
            console.log(res)
          }).catch((err) => {
            console.log(err.toString())
          })
        })
        this.findingFiles = []
      },
      async getAvailableScanner() {
        this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
        this.$axios.get('/misc/scanner').then((res) =>{
          this.availableScanner = res.data
        }).catch((err)=>{
          // Todo
          console.log(err)
        })
      },
    requiredFieldsAreFilled() {
        return Object.values(this.repositoryInformation).every(prop => prop !== '')
      },
    appendNewFile() {
        if (this.findingFile !== null) {
          this.findingFiles.push(this.findingFile)
          this.repositoryInformationUpload = this.repositoryInformation
          this.repositoryInformation = {}
          this.findingFile = null
        }
      }
    }
}
</script>

<template>
  <v-dialog
    v-model="importDialog"
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition"
  >
    <template v-slot:activator="{ props }">
      <div v-bind="props">Import Findings</div>
    </template>
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn v-if="this.findingFiles.length > 0" icon dark @click="cancelImport = true"><v-icon>mdi-close</v-icon></v-btn>
        <v-btn v-else icon dark @click="importDialog = false"><v-icon>mdi-close</v-icon></v-btn>
        <v-dialog v-model="cancelImport" >
          <v-row>
            <v-col></v-col>
            <v-col></v-col>
            <v-col>
              <v-card >
                <v-card-title>Cancel Import</v-card-title>
                <v-card-text>You have unprocessed files.</v-card-text>
                <v-card-text>Do you really want to cancel the import?</v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancelImport = false" color="primary" style="text-align: right">No</v-btn>
                <v-btn @click="importDialog = false" color="primary" style="text-align: right">Yes</v-btn>
              </v-card-actions>
            </v-card></v-col>
            <v-col></v-col>
            <v-col></v-col>
          </v-row>
        </v-dialog>

        <v-toolbar-title>Import Findings</v-toolbar-title>
        <v-spacer></v-spacer>
          <v-btn icon dark @click="uploadFindings()"><v-icon>mdi-import</v-icon>
            <v-badge color="red" :content="this.findingFiles.length" inline></v-badge>
          </v-btn>
      </v-toolbar>
      <v-list lines="two" subheader>
        <v-list-item title="Repository Information"></v-list-item>
        <v-list-item>
          <v-row>
            <v-col>
              <v-text-field
                label="Repository Name*"
                required
                v-model="this.repositoryInformation.repositoryName"
              ></v-text-field>
            </v-col>
          <v-col>
            <v-text-field
              label="Repository Path/Address*"
              required
              v-model="this.repositoryInformation.repositoryPath"
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
                v-model="this.repositoryInformation.scannerType"
              ></v-select>
            </v-col>
            <v-col>
              <v-text-field
                label="Scanner Version*"
                required
                v-model="this.repositoryInformation.scannerVersion"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list lines="two" subheader>
        <v-list-item title="Upload Findings"></v-list-item>
        <v-list-item >
          <v-row>
            <v-col>
              <v-file-input v-if="requiredFieldsAreFilled() === true" v-model="this.findingFile" :rules="this.fileUploadRules" clearable accept=".json" show-size label="File input"></v-file-input>
              <v-file-input v-else :rules="this.fileUploadRules" disabled label="File Input"></v-file-input>
            </v-col>
              <v-col>
                <v-btn v-if="requiredFieldsAreFilled() === true" @click="appendNewFile" color="primary" style="margin-top: 0.5em"><v-icon>mdi-plus</v-icon></v-btn>
                <v-btn v-else color="primary" disabled style="margin-top: 0.5em"><v-icon>mdi-plus</v-icon></v-btn>
              </v-col>
          </v-row>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <!--ImportFindingsProcessUploadLoader :props-dialog="uploadDialog" :props-step-counter="uploadStepCounter"/-->

    </v-card>
  </v-dialog>
</template>
