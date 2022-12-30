<script>

import RepositoryView from "@/views/RepositoryView";

export default {
  data() {
    const repoMockList =[
      { id:  0, name: "Repo1", lastScan: '2022-12-12:00:08:'},
      { id:  1, name: "Repo2", lastScan: '2022-12-12:00:08:'},
      { id:  2, name: "Repo3", lastScan: '2022-12-12:00:08:'},
      { id:  3, name: "Repo4", lastScan: '2022-12-12:00:08:'},
    ]
    return {
      overviewBlock: 'overview-block',
      overviewElement: 'overview-element',
      repoList: 'repo-list',
      repoMockList,
      listItem: 'list-item',
      searchRepo: null
    }
  },
  computed: {
    searchRepoList() {
      if (!this.searchRepo) {
        console.log("Value -1")
        return this.repoMockList
      } else {
        console.log("Other ID")
        console.log(this.searchRepo.id)
        return this.repoMockList.filter((r) => r.id === this.searchRepo.id)
      }
    }
  }
}
</script>

<template>
  <div :class="overviewBlock" >
  <h2>Overview</h2>
    <v-container>
      <v-row no-gutters :class="overviewElement">
        <v-col>
          <v-card title="#Repos" text="1"></v-card>
        </v-col>
        <v-col>
          <v-card title="#Falsch-Positive" text="1"></v-card>
        </v-col>
        <v-col>
          <v-card title="Weitere Infos auf 1 Blick" text="yolo"></v-card>
        </v-col>
      </v-row>

    </v-container>

    <div :class="repoList">
      <h2>Repository List</h2>
      <div>
        <v-autocomplete
          :items="repoMockList"
          v-model="searchRepo"
          item-title="name"
          label="Search Repository"
          prepend-icon="mdi-database-search"
          clearable
          return-object
        />
      </div>

      <v-card class="mx-auto" >
        <v-list>
        <v-list-item
          v-for="repo in searchRepoList"
          :key="repo.id"
          :class="listItem"
        >
          <v-container>
            <v-row >
              <v-col>
                {{ repo.name }}
              </v-col>
              <v-col>
                {{ repo.lastScan }}
              </v-col>
              <v-col>
                <router-link :to="{name: 'RepositoryView', params: {id: repo.id} }"
                             v-slot="{route, navigate}">
                  <v-btn @click="navigate" color="primary">Go to {{ repo.name}}</v-btn>
                </router-link>
              </v-col>
            </v-row>
          </v-container>
        </v-list-item>
        </v-list>
      </v-card>
    </div>
  </div>
</template>

<style>

.overview-block {
  margin: 3em
}

.overview-element {
  margin: 2em
}

.list-item:hover {
  background-color: aliceblue;
}
</style>
