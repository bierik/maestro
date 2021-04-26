<template>
  <LayoutDefault narrow :title="currentMonth">
    <portal to="append-actions">
      <v-btn icon @click="goToday">
        <v-icon>{{ mdiCalendar }}</v-icon>
      </v-btn>
      <v-btn icon @click="prevDate">
        <v-icon>{{ mdiChevronLeft }}</v-icon>
      </v-btn>
      <v-btn icon @click="nextDate">
        <v-icon>{{ mdiChevronRight }}</v-icon>
      </v-btn>
    </portal>
    <FullCalendar ref="calendar" :options="calendarOptions" />
    <AddButton to="/calendar/new" />
  </LayoutDefault>
</template>

<script>
import Vue from 'vue'
import FullCalendar from '@fullcalendar/vue'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import rrulePlugin from '@fullcalendar/rrule'
import interactionPlugin from '@fullcalendar/interaction'
import locale from '@fullcalendar/core/locales/de'
import { mdiChevronLeft, mdiChevronRight, mdiCalendar } from '@mdi/js'
import DateTime from 'luxon/src/datetime'
import { rrulestr, RRule } from 'rrule'
import EventElement from '../../components/task/Event'

const monthFormat = new Intl.DateTimeFormat('de-CH', { month: 'long' })
const EventElementConstructor = Vue.extend(EventElement)

export default {
  name: 'Calendar',
  components: { FullCalendar },
  data() {
    return {
      calendarOptions: {
        plugins: [timeGridPlugin, rrulePlugin, interactionPlugin, dayGridPlugin],
        initialView: 'timeGridWeek',
        eventSources: ['/api/tasks/'],
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
        selectable: true,
        editable: true,
        locale,
        select: this.createTask,
        eventClick: this.editTask,
        eventDrop: this.dragTask,
        eventResize: this.dragTask,
        eventContent: this.renderEvent,
      },
      currentDate: new Date(),
      mdiChevronLeft,
      mdiChevronRight,
      mdiCalendar,
    }
  },
  computed: {
    currentMonth() {
      return monthFormat.format(this.currentDate)
    },
  },
  methods: {
    renderEvent({
      event: {
        extendedProps: { customer },
        title,
      },
      timeText,
    }) {
      const event = new EventElementConstructor({ propsData: { customer, timeText, title } })
      event.$mount()
      return { domNodes: [event.$el] }
    },
    getDuration(start, end) {
      const startDateTime = DateTime.fromJSDate(start)
      const endDateTime = DateTime.fromJSDate(end)
      const duration = endDateTime.diff(startDateTime, ['hours', 'minutes', 'seconds'])
      return duration.toFormat('hh:mm:ss')
    },
    prevDate() {
      const api = this.$refs.calendar.getApi()
      api.prev()
      this.currentDate = api.getDate()
    },
    nextDate() {
      const api = this.$refs.calendar.getApi()
      api.next()
      this.currentDate = api.getDate()
    },
    goToday() {
      const api = this.$refs.calendar.getApi()
      api.today()
      this.currentDate = api.getDate()
    },
    createTask({ start, end }) {
      const duration = this.getDuration(start, end)
      const startDateTime = DateTime.fromJSDate(start).toISO()
      this.$router.push({
        path: '/calendar/new',
        query: { duration, start: startDateTime },
      })
    },
    editTask({ event: { id } }) {
      this.$router.push({ path: `/calendar/edit/${id}` })
    },
    async dragTask({
      event: {
        start,
        end,
        id,
        extendedProps: { rrule_string: rruleString },
      },
      revert,
    }) {
      const duration = this.getDuration(start, end)
      try {
        const rrule = rrulestr(rruleString)
        const updateRrule = new RRule({ freq: rrule.options.freq, dtstart: start, interval: rrule.options.interval })
        await this.$http.$patch(`/tasks/${id}/`, { rrule: updateRrule.toString(), duration })
      } catch (error) {
        this.notifyError('Beim Aktualisieren ist ein Fehler aufgetreten')
        revert()
      }
    },
  },
}
</script>
<style>
.fc-scrollgrid {
  border: 0 !important;
}
</style>
