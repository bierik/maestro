<template>
  <div v-if="monthDisplay" class="primary rounded white--text px-1 caption">{{ customer.full_name }}</div>
  <div v-else class="d-flex flex-column primary px-1 caption" style="height: 100%">
    <span>{{ customer.full_name }}</span>
    <span>{{ title }}</span>
  </div>
</template>

<script>
export default {
  name: 'CalendarEvent',
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
    monthDisplay: {
      type: Boolean,
      default: () => false,
    },
  },
}
</script>
