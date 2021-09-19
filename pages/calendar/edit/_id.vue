<template>
  <LayoutDefault>
    <TaskForm :task="task" />
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
        rrule_string: task.rrule_string,
        title: task.title,
        customer_id: task.customer.id,
      },
    }
  },
}
</script>

<style></style>
