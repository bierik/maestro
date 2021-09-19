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
import { rrulestr, RRule } from 'rrule'
import EventElement from '@/components/task/Event'
import { mapGetters, mapActions } from 'vuex'

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
      const startDateTime = DateTime.fromJSDate(start).toISO()
      this.$router.push({
        path: '/calendar/new',
        query: { duration, start: startDateTime },
      })
    },
    editTask({ event: { id } }) {
      this.$router.push({ path: `/calendar/edit/${id}` })
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
        const rrule = rrulestr(rruleString)
        const updateRrule = new RRule({ freq: rrule.options.freq, dtstart: start, interval: rrule.options.interval })
        await this.$axios.$patch(`/tasks/${id}/`, { rrule: updateRrule.toString(), duration })
        this.refetchEvents()
      } catch (error) {
        this.notifyError('Beim Aktualisieren ist ein Fehler aufgetreten')
        revert()
      }
    },
  },
}
</script>
