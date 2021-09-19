<template>
  <v-tab-item v-bind="$attrs">
    <div class="d-flex justify-end align-center primary white--text">
      <CalendarActionsToday dark />
      <CalendarActionsPrev dark />
      <CalendarActionsNext class="mr-2" dark />
      <span>{{ currentDateString }}</span>
      <v-spacer />
      <CalendarActionsMonth dark />
      <CalendarActionsWeek dark />
    </div>
    <CalendarDefault ref="calendar" :options="calendarOptions" />
  </v-tab-item>
</template>

<script>
import interactionPlugin from '@fullcalendar/interaction'
import { mapGetters } from 'vuex'

export default {
  inheritAttrs: false,
  props: {
    reports: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      calendarOptions: {
        plugins: [interactionPlugin],
        events: this.loadReports,
        eventClick: this.editReport,
      },
    }
  },
  computed: {
    ...mapGetters('calendar', ['currentDateString']),
  },
  methods: {
    editReport({ event: { id } }) {
      this.$router.push(`/reports/${id}`)
    },
    loadReports({ startStr, endStr }, resolve, reject) {
      this.$axios
        .$get(`/customers/${this.$route.params.id}/reports/`, { params: { start: startStr, end: endStr } })
        .then(resolve)
        .catch(reject)
    },
  },
}
</script>
