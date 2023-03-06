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
    FindingListItem,
  },
  data() {
    return {
      headerBlock: 'header-block',
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
      listHeader: 'list-header',
      findingsListContainer: 'findings-list-container',
      findingsListSearchBar: 'findings-list-search-bar',
      findingsList: [],
      searchInput: '',
      overviewData: {},
      loadingFindings: true,
      page: 1,
      pageSize: 10,
      listCount: 0,
      historyList: [],
      bulkEditActive: false,
    }
  },
  methods: {
    initPage: function() {
      this.listCount = this.findingsList.length;
      if (this.listCount < this.pageSize) {
        this.historyList = this.findingsList;
      } else {
        this.historyList = this.findingsList.slice(0, this.pageSize);
      }
    },
    updatePage: function(pageIndex) {
      let start = (pageIndex - 1) * this.pageSize;
      let end = pageIndex * this.pageSize;
      this.historyList = this.findingsList.slice(start, end);
      this.page = pageIndex;
    },
    async getOverviewData() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.id}/count`).then((res) => {
        this.overviewData = {
          documentsAmount: String(res.data['data']['total_number_of_documents']),
          falsePositivesAmount: String(res.data['data']['total_number_of_false_positives']),
          truePositivesAmount: String(res.data['data']['total_number_of_true_positives']),
          lastScanData: this.lastScan,
          totalInitialValues: String(res.data['data']['total_initial_values'])
        }
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
    },
    async getFindingsList() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.id}`).then((res) => {
        this.findingsList = res.data['data']
        this.loadingFindings = false

        this.initPage();
        this.updatePage(this.page);
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
        return this.historyList
      } else {
        return this.historyList.filter((result) => JSON.stringify(result).toLowerCase().includes(this.searchInput.toLowerCase()))
      }
    },
    pages() {
      if (this.pageSize == null || this.listCount == null) return 0;
      return Math.ceil(this.listCount / this.pageSize);
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
          <v-card title="Initial Values" subtitle="total" :text="overviewData.totalInitialValues"></v-card>
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
      <v-container fluid>
        <v-row >
          <v-col></v-col>
          <p style="margin-right: 1em">
            <v-checkbox v-model="bulkEditActive" color="primary" hide-details="true" label="Bulk Edit Status"></v-checkbox>
          </p>
        </v-row>
        <v-list >
          <v-list-item >

            <v-row :class="listHeader" class="text-h6">
              <v-col>File Name</v-col>
              <v-col>Match</v-col>
              <v-col>Current Status</v-col>
              <v-col>Save Date</v-col>
              <v-col style="text-align: right">Details</v-col>
            </v-row>
            <v-divider/>
          </v-list-item>
        </v-list>


        <v-list>
          <FindingListItem v-for="scanResult in filteredFindingsList" :key="scanResult._id" :scan-result="scanResult" :bulk-edit-active="bulkEditActive"/>
          <v-pagination
            v-model="page"
            :length="pages"
            @update:modelValue="updatePage"
          >
          </v-pagination>
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

.findings-list-search-bar {
  justify-content: flex-end
}


</style>
