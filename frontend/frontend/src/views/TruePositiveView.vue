<script>
import {useTokenStore} from "@/store/token";

export default {
  setup() {
    return {
      tokenStore: useTokenStore(),
    }
  },
  created() {
    this.getOverviewData()
  },
  data() {
    return {
      headerBlock: 'header-block',
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
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
          documentsPerRepository: String(res.data['data']['documents_per_repository']),
          totalFalsePositives: String(res.data['data']['total_false_positives']),
          totalTruePositives: String(res.data['data']['total_true_positives']),
        }
        // eslint-disable-next-line no-unused-vars
      }).catch((err) => {/*pass to global error handler*/})
    },
  }
}
</script>

<template>
  <v-toolbar color="primary" :class="headerBlock" density="compact">
    <v-toolbar-title class="text-overline">{{'True Positive Overview'}}</v-toolbar-title>
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
          <v-card title="Repositories" subtitle="total" :text="overviewData.reposAmount"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="False Positives" subtitle="total" :text="overviewData.totalFalsePositives"></v-card>
        </v-col>
        <v-col :class="overviewElement">
          <v-card title="True Positives" subtitle="total" :text="overviewData.totalTruePositives"></v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <v-divider inset></v-divider>
</template>

<style>
.overview-block {
  margin: 3em;
}
.overview-element {
  margin: 0.25em
}
</style>
