<script>

export default {
  props: ['id'],

  data() {
    let mockScanResult= {
      "id": "63a03d0b461bc420de4e638c",
      "scannerType": 0,
      "scannerVersion": "8.15",
      "inputType": 0,
      "repositoryPath": ".",
      "repositoryName": "applications",
      "scanStartTime": "2022-12-16T00:00:00",
      "scanEndTime": "2022-12-16T00:00:00",
      "save_date": "2022-12-19T11:29:31.810344",
      "resultRaw": {
        "Description": "Generic API Key",
        "StartLine": 140,
        "EndLine": 141,
        "StartColumn": 8,
        "EndColumn": 1,
        "Match": "apiGroup: rbac.authorization.k8s.io",
        "Secret": "rbac.authorization.k8s.io",
        "File": "weave-scope/scope.yaml",
        "Commit": "d1925d8548b86acfeb51912909f92756eb687412",
        "Entropy": 3.7230742,
        "Author": "Tibor Pilz",
        "Email": "tibor@pilz.berlin",
        "Date": "2021-09-10T15:57:37+00:00",
        "Message": "Add weave",
        "Tags": [],
        "RuleID": "generic-api-key",
        "Fingerprint": "d1925d8548b86acfeb51912909f92756eb687412:weave-scope/scope.yaml:generic-api-key:140"
      },
      "falsePositive": {
        "isFalsePositive": true,
        "justification": "weil halt",
        "change_date": "2022-12-19T12:43:06.801898"
      }
    }

    return {
      overviewBlock: 'overview-block',
      overviewElementContainer: 'overview-element-container',
      overviewElement: 'overview-element',
      listItem: 'list-item',
      findingsList: 'findings-list',
      mockRepo: {
        id: 0,
        name: "Repo1",
        lastScan: '2022-12-12:00:08:',
        findingsAmount: 14,
        falsePositivesAmount: 4,
        toReviewAmount: 5,
        },
      mockScanResult,
      mockScanResults: [mockScanResult],
      rawResultDialog: false,
      }
  },
  methods: {
    getAdditionalRepoData(repoID) {
      return {
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
    <h2>{{ mockScanResult.repositoryName }}</h2>
    <v-container :class="overviewElementContainer" fluid>
      <v-row no-gutters :class="overviewElement">
        <v-col>
          <v-card title="#Repos" :text="getAdditionalRepoData().findingsAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="#Falsch-Positive" :text="getAdditionalRepoData().falsePositivesAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="#Findings-To-Review" :text="getAdditionalRepoData().toReviewAmount"></v-card>
        </v-col>
        <v-col>
          <v-card title="LastScan" :text="getAdditionalRepoData().lastScan">
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>

    <div :class="findingsList">
    <h2>Findings List</h2>
      <v-card class="mx-auto">
        <v-list>
            <v-list-item
              v-for="scanResult in mockScanResults"
              :key="scanResult.id"
              :class="listItem"
            >
              <v-container fluid>
                <v-row>
                  <v-col>{{ scanResult.id }}</v-col>
                  <v-col>{{scanResult.resultRaw.Fingerprint}}</v-col>
                  <v-col>{{scanResult.save_date}}</v-col>
                  <v-col>
                    <v-icon v-if="!scanResult.falsePositive.isFalsePositive">mdi-check-circle-outline</v-icon>
                    <v-icon v-else>mdi-alert-circle-outline</v-icon>
                  </v-col>
                  <v-col>
                        <v-btn><v-icon>mdi-details</v-icon> Show Raw Result
                          <v-dialog v-model="rawResultDialog" activator="parent">
                            <v-card>
                            <v-card-text>
                              <pre>{{scanResult.resultRaw}}</pre>
                            </v-card-text>
                            <v-card-actions>
                              <v-btn color="primary" block @click="rawResultDialog = false">Close Dialog</v-btn>
                            </v-card-actions>
                          </v-card>
                          </v-dialog>
                        </v-btn>

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
  margin: 3em;
}

.overview-element {
  margin: 2em
}

.findings-list {
  margin: 3em;
}

.list-item:hover {
  background-color: aliceblue;
}
</style>
