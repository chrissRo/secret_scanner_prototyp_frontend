<script>

import {useTokenStore} from "@/store/token";
import moment from "moment/moment";
import FindingListItem from "@/components/FindingListItem";

export default {
  setup() {
    return {
      tokenStore: useTokenStore(),
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
  components:{
    FindingListItem
  },
  data() {
    return {
      headerBlock: 'header-block',
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
      listHeader: 'list-header',
      listItem: 'list-item',
      findingsListContainer: 'findings-list-container',
      findingsListSearchBar: 'findings-list-search-bar',
      findingsList: [],
      searchInput: '',
      overviewData: {},
      loadingFindings: true,
      }
  },
  methods: {
    async getOverviewData() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.id}/count`).then((res) => {
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
      this.$axios.get(`/finding/repository/${this.id}`).then((res) => {
        this.findingsList = res.data['data']
        console.log("fertig")
        this.loadingFindings = false
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
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
      <v-row>
        <v-col/>
        <v-col/>
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
      <v-container fluid v-if="loadingFindings">
        <v-list>
          <v-list-item >
            <v-row :class="listHeader" class="text-h6">
              <v-col>
                File Name
              </v-col>
              <v-col>
                Match
              </v-col>
              <v-col>
                Save Date
              </v-col>
              <v-col style="text-align: right;">
                Details
              </v-col>
            </v-row>
            <v-divider/>
          </v-list-item>
        </v-list>
        <v-progress-circular
          indeterminate
          color="primary">
        </v-progress-circular>
      </v-container>
      <v-container fluid v-else>
        <v-list>
          <v-list-item >
            <v-row :class="listHeader" class="text-h6">
              <v-col>File Name</v-col>
              <v-col>Match </v-col>
              <v-col>Save Date</v-col>
              <v-col style="text-align: right;">Details</v-col>
            </v-row>
            <v-divider/>
          </v-list-item>
          <v-list-item v-for="scanResult in filteredFindingsList" :key="scanResult._id" :class="listItem">
          <FindingListItem :scan-result="scanResult" />
          </v-list-item>
        </v-list>
      </v-container>
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

.list-header {
  margin: auto
}

.list-item:hover {
  background-color: aliceblue;
}

.findings-list-search-bar {
  justify-content: flex-end
}

</style>
