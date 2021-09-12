<template>
  <FullCalendar ref="calendar" :options="calendarOptions" />
</template>

<script>
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import locale from '@fullcalendar/core/locales/de'
import mergeWith from 'lodash/mergeWith'
import get from 'lodash/get'
import isArray from 'lodash/isArray'

export default {
  props: {
    value: {
      type: Date,
      default: () => new Date(),
    },
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
          return objValue.concat(srcValue)
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
  methods: {
    applyCalendarView() {
      if (this.$vuetify.breakpoint.smAndUp) {
        this.api.changeView(get(localStorage, 'view', 'timeGridWeek'))
      } else {
        this.api.changeView('timeGridThreeDay')
      }
    },
    emitCurrentDate() {
      this.$emit('input', this.api.getDate())
    },
    init() {
      this.api = this.$refs.calendar.getApi()
      this.emitCurrentDate()
      this.applyCalendarView()
    },
    prev() {
      this.api.prev()
      this.emitCurrentDate()
    },
    next() {
      this.api.next()
      this.emitCurrentDate()
    },
    today() {
      this.api.today()
      this.emitCurrentDate()
    },
    monthView() {
      localStorage.setItem('view', 'dayGridMonth')
      this.api.changeView('dayGridMonth')
    },
    weekView() {
      localStorage.setItem('view', 'timeGridWeek')
      this.api.changeView('timeGridWeek')
    },
  },
}
</script>

<style>
.fc-scrollgrid {
  border: 0 !important;
}
</style>
