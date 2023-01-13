<script>

import {useTokenStore} from "@/store/token";

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
      overviewElements: 'overview-elements',
      overviewElement: 'overview-element',
      repoList: 'repo-list',
      repoSearchBar: 'repo-search-bar',
      repositoryList: [],
      repositoryList_2: [],
      listItem: 'list-item',
      searchRepo: null,
      overviewData: {}
    }
  },
  methods: {
    async getOverviewData() {

      this.$axios.defaults.headers.Authorization = `Bearer ${this.tokenStore.token}`
      this.$axios.get('/finding/count').then((res) => {
        this.overviewData = {
          documentsAmount: res.data['data']['total_number_of_documents'],
          reposAmount: res.data['data']['total_number_of_distinct_repos'],
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
  <h2>Overview</h2>
    <v-container>
      <v-row no-gutters :class="overviewElements" v-model="overviewData">
          <v-col :class="overviewElement">
            <v-card title="Documents" subtitle="total" :text="overviewData.documentsAmount"></v-card>
          </v-col>
        <v-col :class="overviewElement">
          <v-card title="Repositories" subtitle="total" :text="overviewData.reposAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="Falsch-Positive" subtitle="total" :text="'Todo'"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="Weitere Infos auf 1 Blick" subtitle="total" text="yolo"></v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>

    <div :class="repoList">
      <h2>Repository List</h2>
      <v-container :class="repoSearchBar" fluid>
        <v-row >
          <v-col/>
          <v-col>
            <div>
              <v-autocomplete
                :items="repositoryList"
                v-model="searchRepo"
                item-title="repositoryName"
                label="Search Repository"
                prepend-icon="mdi-database-search"
                clearable
                return-object
              />
            </div>
          </v-col>
        </v-row>
      </v-container>
      <v-card class="mx-auto" >
        <v-list>
          <v-row>
            <v-col>
              RepoName
              <v-divider/>
            </v-col>
            <v-col>
              LastScan
              <v-divider/>
            </v-col>
            <v-list-item>
              Go To
              <v-divider/>
            </v-list-item>
          </v-row>
        <v-list-item
          v-for="repo in searchRepoList"
          :key="repo._id"
          :class="listItem"
        >
          <v-container fluid>
            <v-row >
              <v-col>
                {{ repo.repositoryName }}
              </v-col>
              <v-col>
                {{ repo.scanEndTime }}
              </v-col>
              <v-col>
                <router-link :to="{name: 'RepositoryView', params: {id: repo._id} }"
                             v-slot="{navigate}">
                  <v-btn @click="navigate" color="primary" role="link">Go to {{ repo.repositoryName}}</v-btn>
                </router-link>
              </v-col>
            </v-row>
          </v-container>
        </v-list-item>
        </v-list>
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

.list-item:hover {
  background-color: aliceblue;
}

.repo-search-bar {
  margin: 1em;
  width: 100%;
  justify-content: flex-end
}
</style>
