<template>
  <LayoutDefault :title="currentDateString" narrow>
    <template #prepend-actions>
      <CalendarActionsToday small class="mr-2" />
      <CalendarActionsPrev small />
      <CalendarActionsNext small />
    </template>
    <template #append-actions>
      <CalendarActionsWeek small class="mr-2" />
      <CalendarActionsMonth small />
    </template>
    <CalendarDefault ref="calendar" :options="calendarOptions" />
    <AddButton to="/calendar/new" />
  </LayoutDefault>
</template>

<script>
import Vue from 'vue'
import rrulePlugin from '@fullcalendar/rrule'
import interactionPlugin from '@fullcalendar/interaction'
import DateTime from 'luxon/src/datetime'
import { rrulestr } from 'rrule'
import { mapGetters, mapActions } from 'vuex'
import EventElement from '@/components/task/Event'
import { updateStart } from '@/rrule-helpers'

const EventElementConstructor = Vue.extend(EventElement)

export default {
  name: 'Calendar',
  data() {
    return {
      calendarOptions: {
        plugins: [rrulePlugin, interactionPlugin],
        events: this.loadTasks,
        selectable: true,
        editable: true,
        select: this.createTask,
        eventClick: this.editTask,
        eventDrop: this.dragTask,
        eventResize: this.dragTask,
        eventContent: this.renderEvent,
      },
    }
  },
  head() {
    return {
      title: 'Kalender',
    }
  },
  computed: {
    ...mapGetters('calendar', ['currentDateString']),
    title() {
      const format = new Intl.DateTimeFormat('de-CH', { month: 'long', year: 'numeric' })
      return format.format(this.currentDate)
    },
  },
  methods: {
    ...mapActions('calendar', ['refetchEvents']),
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
    createTask({ start, end }) {
      const duration = this.getDuration(start, end)
      const startDateTime = DateTime.fromJSDate(start).toUTC().toISO()
      this.$router.push({
        path: '/calendar/new',
        query: { duration, start: startDateTime },
      })
    },
    editTask({ event: { id, start } }) {
      const startQueryString = DateTime.fromJSDate(start).toUTC().toISO()
      this.$router.push({ path: `/calendar/edit/${id}`, query: { currentDate: startQueryString } })
    },
    loadTasks({ startStr, endStr }, resolve, reject) {
      this.$axios
        .$get('/tasks/', { params: { start: startStr, end: endStr } })
        .then(resolve)
        .catch(reject)
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
        const rrule = rrulestr(rruleString, { forceset: true })
        await this.$axios.$patch(`/tasks/${id}/`, { rrule: updateStart(rrule, start).toString(), duration })
        this.refetchEvents()
      } catch (error) {
        this.notifyError('Beim Aktualisieren ist ein Fehler aufgetreten')
        revert()
      }
    },
  },
}
</script>
