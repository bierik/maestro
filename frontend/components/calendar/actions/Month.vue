<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="monthView()">
    <v-icon>{{ mdiCalendarMonth }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiCalendarMonth } from '@mdi/js'
import noop from 'lodash/noop'

export default {
  name: 'MonthAction',
  inheritAttrs: false,
  data() {
    return {
      mdiCalendarMonth,
    }
  },
  methods: {
    monthView() {
      this.$router.replace({ query: { ...this.$route.query, calendarView: 'dayGridMonth' } }).catch(noop)
    },
  },
}
</script>
