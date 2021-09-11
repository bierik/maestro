<template>
  <v-btn
    fab
    absolute
    class="rounded-circle main-report-button darken-2"
    :color="hasRunningReport ? 'info' : 'grey'"
    to="/reports"
  >
    <span v-if="hasRunningReport" class="mt-1 caption white--text">{{ runningReportDuration }}</span>
    <v-icon :small="hasRunningReport" color="white">{{ mdiAlarm }}</v-icon>
  </v-btn>
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
    ...mapGetters('report', ['hasRunningReport']),
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
