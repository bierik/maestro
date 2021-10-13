<template>
  <v-list-item :class="{ 'blue lighten-3': hasRunningReport }" to="/reports">
    <v-list-item-icon>
      <v-icon>{{ mdiAlarm }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title>
        {{ reportText }}
      </v-list-item-title>
      <v-list-item-subtitle>
        {{ runningReportCustomer }}
      </v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import { mdiAlarm } from '@mdi/js'
import { mapState, mapGetters } from 'vuex'

export default {
  data() {
    return {
      mdiAlarm,
    }
  },
  computed: {
    ...mapState('report', ['runningReportDuration']),
    ...mapGetters('report', ['hasRunningReport', 'runningReportCustomer']),
    reportText() {
      return this.hasRunningReport ? `Rapport läuft: ${this.runningReportDuration}` : 'Rapport starten'
    },
  },
}
</script>

<style>
.main-report-button {
  top: -40px !important;
  min-width: 0 !important;
  width: 60px !important;
  height: 60px !important;
  left: 50% !important;
  position: absolute !important;
  margin-left: -30px !important;
}
</style>
