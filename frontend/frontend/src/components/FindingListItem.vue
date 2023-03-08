<script>

import {useTokenStore} from "@/store/token";
import moment from "moment";

export default {
  setup() {
    return {
      tokenStore: useTokenStore(),
    }
  },
  emits: [
    "changeFavouriteStatus",
    "changeFalsePositiveStatus"
  ],
  props: {
    scanResult: {},
    bulkEditActive: null
  },
  created() {
    this.findingData = {...this.scanResult}
  },
  data() {
    return {
      findingData: {},
      rawResultDialog: false,
      falsePositiveDialog: false,
      falsePositiveReadOnly: true,
      listItem: 'list-item',
      matchColumn: 'match-column',
      changeStatusFailed: false,
      changeStatusSuccess: false,
      snackbarTimeout: 3000,
      changeStatusErrorMessage: '',
      changeStatusSuccessMessage: '',
    }
  },
  methods: {
    editFalsePositive() {
      this.falsePositiveReadOnly = !this.falsePositiveReadOnly
    },
    async updateFalsePositive(updatedValue) {

      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.put(`/finding/${updatedValue.id}/fp`, updatedValue).then((res) => {
        this.changeStatusSuccessMessage = res.data.message
        this.changeStatusSuccess = true
        this.findingData = res.data.data
        this.$emit('changeFalsePositiveStatus', this.findingData)
      }).catch((err) => {
        this.changeStatusErrorMessage = err.response.data.detail[0].msg
        this.changeStatusFailed = true
      })
      this.editFalsePositive()
    },
    async bulkUpdateFalsePositive(updatedValue) {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`

      updatedValue.falsePositive.isFalsePositive = this.findingData.falsePositive.isFalsePositive
      updatedValue.falsePositive.justification = 'Bulk Edit'
      updatedValue.falsePositive.change_date = Date.now()

      this.$axios.put(`/finding/${updatedValue.id}/fp`, updatedValue).then((res) => {
        this.changeStatusSuccessMessage = res.data.message
        this.changeStatusSuccess = true
        this.findingData = res.data.data
        this.$emit('changeFalsePositiveStatus', this.findingData)
      }).catch((err) => {
        this.changeStatusErrorMessage = err.response.data.detail[0].msg
        this.changeStatusFailed = true
      })
    },
    formatScanDate(scanDateTime){
      return moment(String(scanDateTime)).format('MMMM Do YYYY, HH:mm:ss')
    },
    async changeFavoriteStatus() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.put(`/finding/${this.findingData._id}/fav`, {'isFavourite': !this.findingData.isFavourite }).then(() => {
        this.findingData.isFavourite = !this.findingData.isFavourite
        this.$emit('changeFavouriteStatus', this.findingData)
      }).catch((err) => {
        this.changeStatusErrorMessage = err.response.data.detail[0].msg
        this.changeStatusFailed = true
      })

    }
  }
}

</script>

<template>
  <v-row :class="listItem">
    <v-col>
      <v-icon v-if="findingData.isFavourite" @click="changeFavoriteStatus" color="primary" style="margin-right: 0.5em;">mdi-star</v-icon>
      <v-icon v-else @click="changeFavoriteStatus()" style="margin-right: 0.5em">mdi-star-outline</v-icon>
      <span>
        {{findingData.resultRaw.File.split('\\').pop().split('/').pop()}}
        <v-tooltip :text="`${findingData.resultRaw.File}:${findingData.resultRaw.Commit}`" location="bottom" activator="parent"></v-tooltip>
      </span>
    </v-col>
    <v-col :class="matchColumn">
      <span>
        <pre style="white-space:pre-wrap;" >{{findingData.resultRaw.Match}}</pre>
        <v-tooltip :text="`${findingData.resultRaw.RuleID}`" location="bottom" activator="parent"></v-tooltip>
      </span>
    </v-col>
    <v-col>
      <!--if false-positive is true, then it is an false-positive-->
      <v-chip v-if="findingData.falsePositive.isFalsePositive" class="ma-2" color="primary" text-color="white">False Positive</v-chip>
      <v-chip v-else class="ma-2" color="red" text-color="white">True Positive</v-chip>
      <v-chip v-if="findingData.falsePositive.justification === 'init'" class="ma-2" color="info" text-color="white" >Initial</v-chip>
    </v-col>
    <v-col>{{formatScanDate(findingData.save_date)}}</v-col>
    <v-col style="text-align: right">
      <v-dialog v-model="rawResultDialog" width="50%">
        <template v-slot:activator="{props}">
          <v-btn v-bind="props" color="primary"><v-icon>mdi-details</v-icon> Raw </v-btn>
        </template>
        <v-card >
          <v-card-text>
            <pre style="white-space:pre-wrap;">{{findingData.resultRaw}}</pre>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-col class="text-right">
              <v-btn color="primary" @click="rawResultDialog = false">Close</v-btn>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="falsePositiveDialog" width="500">
        <template v-slot:activator="{props}">
          <v-btn v-bind="props" color="primary" style="margin-left: 1em"><v-icon>mdi-pencil-outline</v-icon> Status</v-btn>
        </template>
        <v-card >
          <v-card-item>
            <v-card-title>Status-Overview</v-card-title>
            <v-card-subtitle>Change Date: {{formatScanDate(findingData.falsePositive.change_date)}}</v-card-subtitle>
            <v-card-text>
              <v-checkbox v-if="falsePositiveReadOnly === true" label="Is False Positive" v-model="findingData.falsePositive.isFalsePositive" disabled></v-checkbox>
              <v-checkbox v-else label="Is False Positive" v-model="findingData.falsePositive.isFalsePositive"></v-checkbox>
              <v-textarea
                :readonly="falsePositiveReadOnly"
                v-model="findingData.falsePositive.justification"
                variant="underlined"
                no-resize
                rows="2"
                label="Reason for change"
              >
              </v-textarea>
            </v-card-text>
          </v-card-item>
          <v-divider></v-divider>
          <v-card-actions>
            <v-col class="text-right">
              <v-btn v-if="falsePositiveReadOnly === true" color="primary" @click="editFalsePositive">Edit</v-btn>
              <v-btn v-else  color="primary" @click="updateFalsePositive({falsePositive: findingData.falsePositive, id: findingData._id})">Save</v-btn>
              <v-btn color="primary" @click="falsePositiveDialog = false">Close</v-btn>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
    <p v-if="bulkEditActive">
      <v-checkbox v-model="findingData.falsePositive.isFalsePositive" color="primary" hide-details="true"
                  @change="bulkUpdateFalsePositive({falsePositive: findingData.falsePositive, id: findingData._id})"></v-checkbox></p>
  </v-row>

  <v-snackbar v-model="changeStatusFailed" :timeout="snackbarTimeout" rounded="pill" color="red" text-color="white">
    {{changeStatusErrorMessage}}
  </v-snackbar>
  <v-snackbar v-model="changeStatusSuccess" :timeout="snackbarTimeout" rounded="pill" color="primary" text-color="white">
    {{changeStatusSuccessMessage}}
  </v-snackbar>

</template>

<style>

.list-item {
  margin: auto
}

.list-item:hover {
  background-color: aliceblue;
}

.match-column {
  width: 20%;
}

</style>
