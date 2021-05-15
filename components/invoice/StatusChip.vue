<template>
  <v-chip x-small :color="color">{{ invoice.status_display }}</v-chip>
</template>

<script>
import { colors } from '@/components/invoice/status'

export default {
  props: {
    invoice: {
      type: Object,
      required: true,
    },
  },
  computed: {
    color() {
      return colors[this.invoice.status]
    },
  },
}
</script>
