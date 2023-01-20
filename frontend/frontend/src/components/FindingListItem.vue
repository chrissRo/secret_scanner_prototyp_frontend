<script>

import {useTokenStore} from "@/store/token";
import moment from "moment";

export default {
  setup() {
    return {
      tokenStore: useTokenStore(),
    }
  },
  props: {
    scanResult: {}
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
      matchColumn: 'match-column'
    }
  },
  methods: {
    editFalsePositive() {
      this.falsePositiveReadOnly = !this.falsePositiveReadOnly
    },
    updateFalsePositive(updatedValue) {
      console.log("Call API-Update -> " + updatedValue.id)
      console.log("New Value -> " + updatedValue.falsePositive.justification)
      console.log("New Status -> " + updatedValue.falsePositive.isFalsePositive)
      this.editFalsePositive()
    },
    formatScanDate(scanDateTime){
      return moment(String(scanDateTime)).format('MMMM Do YYYY, HH:mm:ss')
    }
  }
}

</script>

<template>
  <v-row :class="listItem">
    <v-col>
      <span>
        {{findingData.resultRaw.File.split('\\').pop().split('/').pop()}}
      <v-tooltip :text="findingData.resultRaw.File" location="right" activator="parent"></v-tooltip>
      </span>
    </v-col>
    <v-col :class="matchColumn"><pre style="white-space:pre-wrap;" >{{findingData.resultRaw.Match}}</pre> </v-col>
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
            <v-card-subtitle>Change Date: {{findingData.falsePositive.change_date}}</v-card-subtitle>
            <v-card-text>
              <v-checkbox v-if="falsePositiveReadOnly === true" label="False-Positive" v-model="findingData.falsePositive.isFalsePositive" disabled></v-checkbox>
              <v-checkbox v-else label="False-Positive" v-model="findingData.falsePositive.isFalsePositive"></v-checkbox>
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
              <v-btn v-else  color="primary" @click="updateFalsePositive({falsePositive: scanResult.falsePositive, id: scanResult.id})">Save</v-btn>
              <v-btn color="primary" @click="falsePositiveDialog = false">Close</v-btn>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-row>

</template>

<style>

.list-item {
  margin: auto
}

.list-item:hover {
  background-color: aliceblue;
}

.match-column {
  width: 25%;
}
</style>
