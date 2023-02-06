<script>

import {useTokenStore} from "@/store/token";
import RepositoryListItem from "@/components/RepositoryListItem";

export default {
  setup() {
    return {
      tokenStore: useTokenStore()
    }
  },
  components: {
    RepositoryListItem,
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
          documentsPerRepository: res.data['data']['documents_per_repository'],
          totalFalsePositives: String(res.data['data']['total_false_positives']),
          totalTruePositives: String(res.data['data']['total_true_positives']),
          totalInitialValues: String(res.data['data']['total_initial_values'])
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
          <v-card title="False Positives" subtitle="total" :text="overviewData.totalFalsePositives"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="True Positives" subtitle="total" :text="overviewData.totalTruePositives"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="Initial Values" subtitle="total" :text="overviewData.totalInitialValues"></v-card>
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
                Numbers
              </v-col>
              <v-col style="text-align: right;">
                Details
              </v-col>
            </v-row>
            <v-divider/>
          </v-list-item>

        <RepositoryListItem
          v-for="repo in searchRepoList"
          :key="repo._id"
          :class="listItem" :repository="repo" :overview-data="this.overviewData"/>
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
