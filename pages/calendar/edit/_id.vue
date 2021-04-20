<template>
  <LayoutDefault>
    <TaskForm :task="task" />
  </LayoutDefault>
</template>

<script>
export default {
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const task = await $http.$get(`tasks/${id}/`)
    return { task }
  },
}
</script>

<style></style>
