<template>
  <FullCalendar ref="calendar" :options="calendarOptions" />
</template>

<script>
import '@fullcalendar/core'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import locale from '@fullcalendar/core/locales/de'
import mergeWith from 'lodash/mergeWith'
import isArray from 'lodash/isArray'
import { mapMutations, mapActions } from 'vuex'

export default {
  props: {
    options: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      api: null,
      defaultOptions: {
        plugins: [timeGridPlugin, dayGridPlugin],
        initialView: 'timeGridThreeDay',
        headerToolbar: false,
        height: '100%',
        displayEventEnd: true,
        nowIndicator: true,
        weekNumbers: true,
        allDaySlot: false,
        slotMinTime: '06:00:00',
        slotMaxTime: '20:00:00',
        slotDuration: '00:15:00',
        scrollTime: '08:00:00',
        viewDidMount: this.init,
        locale,
        views: {
          timeGridThreeDay: {
            type: 'timeGrid',
            duration: { days: 3 },
          },
        },
      },
    }
  },
  computed: {
    calendarOptions() {
      return mergeWith(this.defaultOptions, this.options, (objValue, srcValue) => {
        if (isArray(objValue)) {
          return [...objValue, ...srcValue]
        }
      })
    },
  },
  watch: {
    '$vuetify.breakpoint.smAndUp': {
      handler() {
        this.applyCalendarView()
      },
    },
  },
  mounted() {
    document.addEventListener('swiped-left', this.next)
    document.addEventListener('swiped-right', this.prev)
  },
  destroyed() {
    document.removeEventListener('swiped-left', this.next)
    document.removeEventListener('swiped-right', this.prev)
  },
  methods: {
    ...mapMutations('calendar', ['setApi']),
    ...mapActions('calendar', ['applyDesktopView', 'applyMobileView', 'prev', 'next']),
    applyCalendarView() {
      if (this.$vuetify.breakpoint.smAndUp) {
        this.applyDesktopView()
      } else {
        this.applyMobileView()
      }
    },
    init() {
      this.setApi(this.$refs.calendar.getApi())
      this.applyCalendarView()
    },
  },
}
</script>

<style>
.fc-scrollgrid {
  border: 0 !important;
}

.fc-day {
  overflow: hidden;
}
</style>
