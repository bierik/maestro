<template>
  <LayoutDefault>
    <TaskForm v-model="task" :current-date="currentDate" />
  </LayoutDefault>
</template>

<script>
export default {
  async asyncData({
    $axios,
    route: {
      params: { id },
    },
  }) {
    const task = await $axios.$get(`tasks/${id}/`)
    return {
      task: {
        id: task.id,
        duration: task.duration,
        rrule: task.rrule,
        title: task.title,
        customer_id: task.customer.id,
      },
    }
  },
  head() {
    return {
      title: ['Auftrag', this.task.title].join(' - '),
    }
  },
  computed: {
    currentDate() {
      return this.$route.query.currentDate
    },
  },
}
</script>

<style></style>
