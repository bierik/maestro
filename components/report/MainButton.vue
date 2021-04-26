<template>
  <v-btn fab absolute class="rounded-circle main-report-button darken-2" color="grey" to="/reports">
    <span v-if="runningReport" class="mt-1 caption white--text">{{ runningReportDuration }}</span>
    <v-icon :small="hasRunningReport" color="white">{{ mdiAlarm }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiAlarm } from '@mdi/js'
import { mapState, mapGetters } from 'vuex'
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      mdiAlarm,
      runningReportDuration: null,
      runningReportDurationInterval: null,
    }
  },
  computed: {
    ...mapState('report', ['runningReport']),
    ...mapGetters('report', ['hasRunningReport']),
  },
  mounted() {
    this.computeRunningReportDuration()
    this.runningReportDurationInterval = setInterval(() => {
      this.computeRunningReportDuration()
    }, 60 * 1000)
  },
  destroyed() {
    clearInterval(this.runningReportDurationInterval)
  },
  methods: {
    computeRunningReportDuration() {
      if (this.hasRunningReport) {
        const start = DateTime.fromISO(this.runningReport.start)
        this.runningReportDuration = DateTime.local().diff(start).toFormat('hh:mm')
      } else {
        this.runningReportDuration = ''
      }
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
