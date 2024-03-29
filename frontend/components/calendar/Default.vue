<template>
  <FullCalendar ref="calendar" :options="calendarOptions" />
</template>

<script>
import '@fullcalendar/core'
import locale from '@fullcalendar/core/locales/de'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import isArray from 'lodash/isArray'
import mergeWith from 'lodash/mergeWith'
import { mapMutations, mapActions } from 'vuex'

export default {
  name: 'DefaultCalendar',
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
        timeZone: 'UTC',
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
    $route: {
      handler({ query: { calendarView, calendarViewDate } }) {
        setTimeout(() => {
          this.setView({ calendarView, calendarViewDate })
        }, 0)
      },
      immediate: true,
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
    ...mapActions('calendar', ['setView', 'prev', 'next']),
    init() {
      this.setApi(this.$refs.calendar.getApi())
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

.fc-timegrid-event .fc-event-main,
.fc-timegrid-event {
  padding: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  border: 0 !important;
  background: transparent !important;
}
</style>
