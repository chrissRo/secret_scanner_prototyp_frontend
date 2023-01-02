<script>
export default {
  props: ['id'],
  data() {
    return {
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
      mockRepo: { id:  0,
        name: "Repo1",
        lastScan: '2022-12-12:00:08:',
        findingsAmount: 14,
        falsePositivesAmount: 4,
        toReviewAmount: 5
      }
    }
  },
  methods: {
    getRepoData(repoID) {
      return {
        repoID: this.mockRepo.id,
        repoName: this.mockRepo.name,
        lastScan: this.mockRepo.lastScan,
        findingsAmount: this.mockRepo.findingsAmount,
        falsePositivesAmount: this.mockRepo.falsePositivesAmount,
        toReviewAmount: this.mockRepo.toReviewAmount
      }
    }

  }
}
</script>


<template>
  <div :class="overviewBlock" >
    <h2>{{ getRepoData().repoName }}</h2>
    <v-container :class="overviewElementContainer" fluid>
      <v-row no-gutters :class="overviewElement">
        <v-col>
          <v-card title="#Repos" :text="getRepoData().findingsAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="#Falsch-Positive" :text="getRepoData().falsePositivesAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="#Findings-To-Review" :text="getRepoData().toReviewAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="LastScan" :text="getRepoData().lastScan">
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style>
.overview-block {
  margin: 3em;
}

.overview-element {
  margin: 2em
}
</style>
