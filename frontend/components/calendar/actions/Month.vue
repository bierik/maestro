<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="monthView()">
    <v-icon>{{ mdiCalendarMonth }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiCalendarMonth } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  name: 'MonthAction',
  inheritAttrs: false,
  data() {
    return {
      mdiCalendarMonth,
    }
  },
  methods: {
    ...mapActions('calendar', ['monthView']),
  },
}
</script>
