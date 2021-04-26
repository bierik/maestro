<template>
  <div class="d-flex flex-column">
    <strong>{{ title }}</strong>
    <strong>{{ customer.full_name }}</strong>
    <span>{{ timeText }}</span>
  </div>
</template>

<script>
export default {
  name: 'Event',
  props: {
    customer: {
      type: Object,
      default: () => ({}),
    },
    timeText: {
      type: String,
      default: () => '',
    },
    title: {
      type: String,
      default: () => '',
    },
  },
}
</script>
