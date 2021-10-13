<template>
  <v-btn fab absolute :color="hasRunningReport ? 'info' : 'grey'" to="/reports">
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
