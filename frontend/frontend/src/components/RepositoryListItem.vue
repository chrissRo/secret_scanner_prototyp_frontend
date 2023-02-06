<script>
import moment from "moment/moment";
import scannerType from "@/api/apiModel";
import {useTokenStore} from "@/store/token";

export default {
  props: {
    repository: {},
    overviewData: {}
  },
  setup() {
    return {
      tokenStore: useTokenStore(),
    }
  },
  created: function () {
    this.repo = {...this.repository}
    this.getOverviewData()
  },
  data() {
    return {
      repo: {},
      repoOverviewData: {}
    }
  },
  methods: {
    formatScanDate(scanDateTime){
      return moment(String(scanDateTime)).format('MMMM Do YYYY, HH:mm:ss')
    },
    getScannerString(type, version){
      switch (type) {
        case scannerType.Gitleaks:
          return 'Gitleaks ' + version
        default:
          return 'Unknown Scanner'
      }
    },
    getDocumentCountForRepo(repoName){
      let data = this.overviewData.documentsPerRepository.filter((r) => r['_id'] === repoName)
      return data[0]['count']
    },
    async getOverviewData() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get(`/finding/repository/${this.repo.repositoryName}/count`).then((res) => {
        this.repoOverviewData = {
          falsePositivesAmount: String(res.data['data']['total_number_of_false_positives']),
          truePositivesAmount: String(res.data['data']['total_number_of_true_positives']),
          totalInitialValues: String(res.data['data']['total_initial_values'])
        }
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
    },
  }
}
</script>


<template>
  <v-row >
    <v-col>
      {{ repo.repositoryName }}
    </v-col>
    <v-col>
      {{ getScannerString(repo.scannerType, repo.scannerVersion)}}
    </v-col>
    <v-col>
      {{ formatScanDate(repo.scanEndTime) }}
    </v-col>
    <v-col>
      <v-chip lable="init" class="mr-2" color="primary" text-color="white" >initial: {{this.repoOverviewData.totalInitialValues}}</v-chip>
      <v-chip lable="true" class="mr-2" color="red" text-color="white" >true: {{this.repoOverviewData.truePositivesAmount}}</v-chip>
      <v-chip lable="false" class="mr-2" color="info" text-color="white" >false: {{this.repoOverviewData.falsePositivesAmount}}</v-chip>
    </v-col>
    <v-col v-if="repo.repositoryPath != '.'" style="text-align: right;">
      Manual Import
      <router-link :to="{name: 'RepositoryFindingView', params: {id: repo.repositoryName, lastScan: repo.scanEndTime}}"
                   v-slot="{navigate}"
                   style="margin-left: 1em">
        <v-btn @click="navigate" color="primary" role="link">
          <v-icon>mdi-pencil-box-multiple-outline</v-icon>
        </v-btn>
      </router-link>
    </v-col>
    <v-col v-else style="text-align: right;">
      <v-btn href="https://gitlab.com/TODO" color="primary">
        <v-icon>mdi-gitlab</v-icon>
      </v-btn>
      <router-link :to="{name: 'RepositoryFindingView', params: {id: repo.repositoryName, lastScan: repo.scanEndTime}}"
                   v-slot="{navigate}"
                   style="margin-left: 1em">
        <v-btn @click="navigate" color="primary" role="link">
          <v-icon>mdi-pencil-box-multiple-outline</v-icon>
        </v-btn>
      </router-link>
    </v-col>
  </v-row>
</template>

<style>

</style>

