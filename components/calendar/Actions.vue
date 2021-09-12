<template>
  <div class="d-flex">
    <v-btn icon class="inherit-color" @click="weekView()">
      <v-icon>{{ mdiCalendarWeek }}</v-icon>
    </v-btn>
    <v-btn icon class="inherit-color" @click="monthView()">
      <v-icon>{{ mdiCalendarMonth }}</v-icon>
    </v-btn>
    <v-btn icon class="inherit-color" @click="today()">
      <v-icon>{{ mdiCalendarToday }}</v-icon>
    </v-btn>
    <v-btn icon class="inherit-color" @click="prev()">
      <v-icon>{{ mdiChevronLeft }}</v-icon>
    </v-btn>
    <v-btn icon class="inherit-color" @click="next()">
      <v-icon>{{ mdiChevronRight }}</v-icon>
    </v-btn>
  </div>
</template>

<script>
import { mdiChevronLeft, mdiChevronRight, mdiCalendarToday, mdiCalendarMonth, mdiCalendarWeek } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      mdiChevronLeft,
      mdiChevronRight,
      mdiCalendarToday,
      mdiCalendarMonth,
      mdiCalendarWeek,
    }
  },
  methods: {
    ...mapActions('calendar', ['monthView', 'weekView', 'today', 'prev', 'next']),
  },
}
</script>
<style>
.inherit-color {
  color: inherit !important;
}
</style>
