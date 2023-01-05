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
      findingsListSearchBar: 'findings-list-search-bar',
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
      falsePositiveDialog: false,
      falsePositiveReadOnly: true,
      searchInput: '',
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
    },
    editFalsePositive() {
      this.falsePositiveReadOnly = !this.falsePositiveReadOnly
    },
    updateFalsePositive(updatedValue) {
      console.log("Call API-Update -> " + updatedValue.id)
      console.log("New Value -> " + updatedValue.falsePositive.justification)
      console.log("New Status -> " + updatedValue.falsePositive.isFalsePositive)
      this.editFalsePositive()
    }
  },
  computed: {
    filteredScanResults() {
      if (this.searchInput) {
        return this.mockScanResults.filter((result) => JSON.stringify(result).toLowerCase().includes(this.searchInput.toLowerCase()))
      } else {
        return this.mockScanResults
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
      <v-container :class="findingsListSearchBar" fluid>
        <v-row >
          <v-col/>
          <v-col>
              <v-text-field
                clearable
                label="Search"
                prepend-icon="mdi-database-search"
                v-model="searchInput"
              ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
      <v-card class="mx-auto">
        <v-list>
            <v-list-item
              v-for="scanResult in filteredScanResults"
              :key="scanResult.id"
              :class="listItem"
            >
              <v-container fluid>
                <v-row>
                  <v-col>{{ scanResult.resultRaw.File }}</v-col>
                  <v-col>{{scanResult.resultRaw.Match}}</v-col>
                  <v-col>{{scanResult.save_date}}</v-col>
                  <v-col>
                        <v-btn><v-icon>mdi-details</v-icon> Show Raw Result
                          <v-dialog v-model="rawResultDialog" activator="parent" width="50%">
                            <v-card >
                            <v-card-text>
                              <pre style="white-space:pre-wrap;">{{scanResult.resultRaw}}</pre>
                            </v-card-text>
                              <v-divider></v-divider>
                            <v-card-actions>
                              <v-col class="text-right">
                                <v-btn color="primary" @click="rawResultDialog = false">Close</v-btn>
                              </v-col>
                            </v-card-actions>
                          </v-card>
                          </v-dialog>
                        </v-btn>
                  </v-col>
                  <v-col>
                    <v-btn>
                      <v-icon v-if="scanResult.falsePositive.isFalsePositive">mdi-check-circle-outline</v-icon>
                      <v-icon v-else>mdi-alert-circle-outline</v-icon>
                      Review Status
                      <v-dialog v-model="falsePositiveDialog" activator="parent" width="500">
                        <v-card >
                          <v-card-item>
                            <v-card-title>Status-Overview</v-card-title>
                            <v-card-subtitle>Change Date: {{scanResult.falsePositive.change_date}}</v-card-subtitle>
                            <v-card-text>
                              <v-checkbox v-if="falsePositiveReadOnly === true" label="False-Positive" v-model="scanResult.falsePositive.isFalsePositive" disabled></v-checkbox>
                              <v-checkbox v-else label="False-Positive" v-model="scanResult.falsePositive.isFalsePositive"></v-checkbox>
                              <v-textarea
                                :readonly="falsePositiveReadOnly"
                                v-model="scanResult.falsePositive.justification"
                                variant="underlined"
                                no-resize
                                rows="2"
                                label="Reason for change"
                              >
                              </v-textarea>
                            </v-card-text>
                          </v-card-item>
                          <v-divider></v-divider>
                          <v-card-actions>
                            <v-col class="text-right">
                              <v-btn v-if="falsePositiveReadOnly === true"  color="primary" @click="editFalsePositive">Edit</v-btn>
                              <v-btn v-else  color="primary" @click="updateFalsePositive({falsePositive: scanResult.falsePositive, id: scanResult.id})">Save</v-btn>
                              <v-btn color="primary" @click="falsePositiveDialog = false">Close</v-btn>
                            </v-col>
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
