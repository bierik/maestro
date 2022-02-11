export default function ({ $vuetify, redirect, route }) {
  const hasCalendarView = !!route.query.calendarView
  if (!hasCalendarView) {
    const calendarView = $vuetify.breakpoint.smAndUp ? 'dayGridMonth' : 'timeGridThreeDay'
    redirect({ name: route.name, params: route.params, hash: route.hash, query: { ...route.query, calendarView } })
  }
}
