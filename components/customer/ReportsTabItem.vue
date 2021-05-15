<template>
  <v-tab-item v-bind="$attrs">
    <CalendarDefault ref="calendar" :options="calendarOptions" />
  </v-tab-item>
</template>

<script>
import interactionPlugin from '@fullcalendar/interaction'

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
        eventSources: [`/api/customers/${this.$route.params.id}/reports/`],
        eventClick: this.editReport,
      },
    }
  },
  methods: {
    editReport({ event: { id } }) {
      this.$router.push(`/reports/${id}`)
    },
  },
}
</script>
