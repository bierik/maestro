<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="weekView()">
    <v-icon>{{ mdiCalendarWeek }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiCalendarWeek } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  inheritAttrs: false,
  data() {
    return {
      mdiCalendarWeek,
    }
  },
  methods: {
    ...mapActions('calendar', ['weekView']),
  },
}
</script>
