<script>
import moment from "moment/moment";
import scannerType from "@/api/apiModel";
import {useTokenStore} from "@/store/token";
import repositoryIcons from "@/styles/repositoryIcons";

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
    getRepositoryIcon(repositoryPath){
      let icon = repositoryIcons['default']
      try{
        const domain = new URL(repositoryPath).hostname
        if(domain){
          // handle if domain contains subdomain
          let hostname = domain.split('.')
          if(hostname.length === 2){
            hostname = hostname[0]
          } else {
            hostname = hostname[1]
          }
          icon = repositoryIcons[hostname]
        }
        // eslint-disable-next-line no-unused-vars
      }catch (TypeError){ /* just ignore, default icon already set */ }
      return icon
    }
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
    <v-col v-if="repo.repositoryPath === '.'" style="text-align: right;">
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
      <v-btn :href="repo.repositoryPath" target="_blank" color="primary">
        <v-icon>{{getRepositoryIcon(repo.repositoryPath)}}</v-icon>
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

