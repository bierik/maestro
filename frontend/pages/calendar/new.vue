<template>
  <LayoutDefault>
    <TaskForm v-model="task" />
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import { RRule, RRuleSet } from 'rrule'

function createTask({ start = DateTime.utc().toISO(), duration = '01:00:00' } = {}) {
  const dtstart = DateTime.fromISO(start).toJSDate()
  const rrule = new RRuleSet()
  rrule.rrule(new RRule({ freq: RRule.WEEKLY, interval: 1, dtstart }))

  return {
    rrule: rrule.toString(),
    duration,
  }
}

export default {
  name: 'NewTask',
  asyncData({ route }) {
    return {
      task: createTask(route.query),
    }
  },
  head() {
    return {
      title: 'Neuer Auftrag',
    }
  },
}
</script>
