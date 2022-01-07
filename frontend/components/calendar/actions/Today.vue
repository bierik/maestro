<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="today()">
    <v-icon>{{ mdiCalendarToday }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiCalendarToday } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  name: 'TodayAction',
  inheritAttrs: false,
  data() {
    return {
      mdiCalendarToday,
    }
  },
  methods: {
    ...mapActions('calendar', ['today']),
  },
}
</script>
