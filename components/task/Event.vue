<template>
  <div class="d-flex flex-column">
    <strong>{{ customerName }}</strong>
    <span>{{ timeText }}</span>
  </div>
</template>

<script>
export default {
  name: 'Event',
  props: {
    customerName: {
      type: String,
      default: () => '',
    },
    timeText: {
      type: String,
      default: () => '',
    },
  },
}
</script>
