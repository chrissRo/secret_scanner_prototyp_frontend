<script>
export default {
  data() {

    const repoMockList =[
      { id:  0, repoName: "Repo1"},
      { id:  1, repoName: "Repo2"},
      { id:  2, repoName: "Repo3"},
      { id:  3, repoName: "Repo4"},
    ]

    return {
      overviewBlock: 'overview-block',
      overviewElement: 'overview-element',
      repoList: 'repo-list',
      repoMockList
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
      <v-card class="mx-auto" >
        <v-list >
            <v-list-item
              v-for="repo in repoMockList"
              :key="repo.id"
              :title="repo.repoName"
              >
              <v-checkbox label="Falsch-Positiv" color="primary" value="info"></v-checkbox>
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
</style>
