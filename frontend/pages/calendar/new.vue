<template>
  <LayoutDefault>
    <TaskForm v-model="task" />
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  name: 'NewTask',
  data() {
    return {
      task: {
        start: this.$route.query.start || DateTime.local().toFormat("yyyy-MM-dd'T'HH:mm"),
        duration: this.$route.query.duration || '01:00:00',
        frequency: 'WEEKLY',
      },
    }
  },
  head() {
    return {
      title: 'Neuer Auftrag',
    }
  },
}
</script>
