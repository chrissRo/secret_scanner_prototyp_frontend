<script>

import {useTokenStore} from "@/store/token";
import moment from "moment";
import scannerType from "@/api/apiModel";

export default {
  setup() {
    return {
      tokenStore: useTokenStore()
    }
  },
  created() {
    this.getOverviewData()
    this.getRepositoryList()
  },
  data() {
    return {
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElements: 'overview-elements',
      overviewElement: 'overview-element',
      repoList: 'repo-list',
      repoSearchBar: 'repo-search-bar',
      repositoryList: [],
      listItem: 'list-item',
      listHeader: 'list-header',
      searchRepo: null,
      overviewData: {},
    }
  },
  methods: {
    async getOverviewData() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get('/finding/count').then((res) => {
        this.overviewData = {
          documentsAmount: String(res.data['data']['total_number_of_documents']),
          reposAmount: String(res.data['data']['total_number_of_distinct_repos']),
          documentsPerRepository: res.data['data']['documents_per_repository']
        }
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
  },
    async getRepositoryList() {
      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get('/finding/overview').then((res) => {
        this.repositoryList = res.data["data"]
      }).catch((err) => {
        console.log(err)
      })
    },
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
  },
  computed: {
    searchRepoList() {
      if (!this.searchRepo) {
        return this.repositoryList
      } else {
        return this.repositoryList.filter((r) => r._id === this.searchRepo._id)
      }
    }
  }
}
</script>

<template>
  <div :class="overviewBlock" >
    <v-toolbar color="primary">
      <v-toolbar-title class="text-h5">Overview</v-toolbar-title>
    </v-toolbar>


    <v-container :class="overviewElementContainer" fluid>
      <v-row no-gutters :class="overviewElements" v-model="overviewData">
          <v-col :class="overviewElement">
            <v-card title="Documents" subtitle="total" :text="overviewData.documentsAmount"></v-card>
          </v-col>
        <v-col :class="overviewElement">
          <v-card title="Repositories" subtitle="total" :text="overviewData.reposAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="False-Positives" subtitle="total" :text="'Todo'"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="Weitere Infos auf 1 Blick" subtitle="total" text="yolo"></v-card>
        </v-col>
      </v-row>
    </v-container>


  </div>
  <v-divider inset></v-divider>

  <div :class="repoList">
    <v-toolbar color="primary">
      <v-toolbar-title class="text-h5">Repository List</v-toolbar-title>
    </v-toolbar>
      <v-container :class="repoSearchBar" fluid>
        <v-row >
          <v-col/>
          <v-col/>
          <v-col/>
          <v-col>
              <v-autocomplete
                :items="repositoryList"
                v-model="searchRepo"
                item-title="repositoryName"
                label="Search Repository"
                prepend-icon="mdi-database-search"
                clearable
                return-object
              />
          </v-col>
        </v-row>
      </v-container >

      <v-card class="mx-auto" >
        <v-container fluid>
        <v-list>
          <v-list-item >
            <v-row :class="listHeader" class="text-h6">
              <v-col>
                Repository Name
              </v-col>
              <v-col>
                Scanner Information
              </v-col>
              <v-col>
                Date and time of last scan
              </v-col>
              <v-col>
                Number of scan-results
              </v-col>
              <v-col style="text-align: right;">
                Details
              </v-col>
            </v-row>
            <v-divider/>
          </v-list-item>
        <v-list-item
          v-for="repo in searchRepoList"
          :key="repo._id"
          :class="listItem">
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
        </v-list-item>
        </v-list>
        </v-container>
      </v-card>
    </div>

</template>

<style>

.overview-block {
  margin: 3em
}

.repo-list {
  margin: 3em;
}
.overview-elements {
  margin: 1em
}

.overview-element {
  margin: 0.25em
}

.list-header {
  margin:auto
}

.list-item {
  margin: auto
}

.list-item:hover {
  background-color: aliceblue;
}

.repo-search-bar {
  margin: 1em;
  width: 100%;
  justify-content: flex-end
}
</style>
