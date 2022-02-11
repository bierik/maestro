<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="applyWeekView()">
    <v-icon>{{ mdiCalendarWeek }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiCalendarWeek } from '@mdi/js'

export default {
  name: 'WeekAction',
  inheritAttrs: false,
  data() {
    return {
      mdiCalendarWeek,
    }
  },
  methods: {
    applyWeekView() {
      this.$vuetify.breakpoint.smAndUp
        ? this.$router.replace({
            query: { ...this.$route.query, calendarView: 'timeGridWeek' },
          })
        : this.$router.replace({
            query: { ...this.$route.query, calendarView: 'timeGridThreeDay' },
          })
    },
  },
}
</script>
