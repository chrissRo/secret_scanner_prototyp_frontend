<script>
import moment from "moment/moment";
import scannerType from "@/api/apiModel";

export default {
  props: {
    repository: {},
    overviewData: {}
  },
  created() {
    this.repo = {...this.repository}
  },
  data() {
    return {
      repo: {}
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
      {{getDocumentCountForRepo(repo.repositoryName)}}
    </v-col>
    <v-col v-if="repo.repositoryPath != '.'" style="text-align: right;">
      Manual Import
      <router-link :to="{name: 'RepositoryView', params: {id: repo._id, lastScan: repo.scanEndTime}}"
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
      <router-link :to="{name: 'RepositoryView', params: {id: repo.repositoryName, lastScan: repo.scanEndTime}}"
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

