<script>

import {useTokenStore} from "@/store/token";
import moment from "moment/moment";

export default {
  setup() {
    return {
      tokenStore: useTokenStore()
    }
  },
  created() {
    this.getOverviewData()
    this.getFindingsList()
  },
  props: {
    id: String,
    lastScan: String
  },
  data() {
    return {
      headerBlock: 'header-block',
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
      listItem: 'list-item',
      findingsListContainer: 'findings-list-container',
      findingsListSearchBar: 'findings-list-search-bar',
      findingsList: [],
      rawResultDialog: [],
      falsePositiveDialog: false, // TODO fix like rawResultDialog
      falsePositiveReadOnly: true,
      searchInput: '',
      overviewData: {}
      }
  },
  methods: {
    async getOverviewData() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.id}/count/`).then((res) => {
        this.overviewData = {
          documentsAmount: String(res.data['data']['total_number_of_documents']),
          falsePositivesAmount: String(res.data['data']['total_number_of_false_positives']),
          truePositivesAmount: String(res.data['data']['total_number_of_true_positives']),
          toReviewAmount: String(res.data['data']['total_number_of_todos']),
          lastScanData: this.lastScan
        }
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
    },
    async getFindingsList() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.id}/`).then((res) => {
        this.findingsList = res.data['data']
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
    },
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
  },
  computed: {
    filteredFindingsList() {
      if (!this.searchInput) {
        return this.findingsList
      } else {
        return this.findingsList.filter((result) => JSON.stringify(result).toLowerCase().includes(this.searchInput.toLowerCase()))
      }
    }
  }
}
</script>

<template>
  <v-toolbar color="primary" :class="headerBlock" density="compact">
    <v-toolbar-title class="text-overline">{{ 'Repository: ' + id }}</v-toolbar-title>
  </v-toolbar>
  <div :class="overviewBlock" >
    <v-toolbar color="primary">
      <v-toolbar-title class="text-h5">Overview</v-toolbar-title>
    </v-toolbar>

    <v-container :class="overviewElementContainer" fluid>
      <v-row no-gutters :class="overviewElement" v-model="overviewData">
        <v-col :class="overviewElement">
          <v-card title="Documents" subtitle="total" :text="overviewData.documentsAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="False-Positives" subtitle="total" :text="overviewData.falsePositivesAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="True-Positives" subtitle="total" :text="overviewData.truePositivesAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="To-Review" subtitle="total" :text="overviewData.toReviewAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="Date of Last Scan" subtitle="Timestamp" :text="formatScanDate(lastScan)"></v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <v-divider inset></v-divider>

  <div :class="findingsListContainer">
    <v-toolbar color="primary">
      <v-toolbar-title class="text-h5">Findings List</v-toolbar-title>
    </v-toolbar>
      <v-container :class="findingsListSearchBar" fluid>
        <v-row >
          <v-col/>
          <v-col>
              <v-text-field
                clearable
                label="Search"
                prepend-icon="mdi-database-search"
                v-model="searchInput"
              ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
      <v-card class="mx-auto">
        <v-list>
            <v-list-item
              v-for="(scanResult, index) in filteredFindingsList"
              :key="scanResult._id"
              :class="listItem"
            >
              <v-container fluid>
                <v-row>
                  <v-col>{{scanResult.resultRaw.File}}</v-col>
                  <v-col>{{scanResult.resultRaw.Match}}</v-col>
                  <v-col>{{scanResult.save_date}}</v-col>
                  <v-col>
                    <v-dialog v-model="rawResultDialog[index]" width="50%">
                      <template v-slot:activator="{props}">
                        <v-btn v-bind="props"><v-icon>mdi-details</v-icon> Show Raw Result</v-btn>
                      </template>
                      <v-card >
                        <v-card-text>
                          <pre style="white-space:pre-wrap;">{{scanResult.resultRaw}}</pre>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                          <v-col class="text-right">
                            <v-btn color="primary" @click="rawResultDialog[index] = false">Close</v-btn>
                          </v-col>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>

                  </v-col>
                  <v-col>
                    <v-btn>
                      <v-icon v-if="scanResult.falsePositive.isFalsePositive">mdi-check-circle-outline</v-icon>
                      <v-icon v-else>mdi-alert-circle-outline</v-icon>
                      Review Status
                      <v-dialog v-model="falsePositiveDialog" activator="parent" width="500">
                        <v-card >
                          <v-card-item>
                            <v-card-title>Status-Overview</v-card-title>
                            <v-card-subtitle>Change Date: {{scanResult.falsePositive.change_date}}</v-card-subtitle>
                            <v-card-text>
                              <v-checkbox v-if="falsePositiveReadOnly === true" label="False-Positive" v-model="scanResult.falsePositive.isFalsePositive" disabled></v-checkbox>
                              <v-checkbox v-else label="False-Positive" v-model="scanResult.falsePositive.isFalsePositive"></v-checkbox>
                              <v-textarea
                                :readonly="falsePositiveReadOnly"
                                v-model="scanResult.falsePositive.justification"
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
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-list-item>
        </v-list>
      </v-card>
    </div>

</template>

<style>

.header-block {

}

.overview-block {
  margin: 3em;
}

.overview-element {
  margin: 0.25em
}

.findings-list-container {
  margin: 3em;
}

.list-item:hover {
  background-color: aliceblue;
}

</style>
