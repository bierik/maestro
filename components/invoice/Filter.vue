<template>
  <v-chip-group v-model="filter" multiple>
    <v-chip filter color="created" :value="status.CREATED">Erstellt</v-chip>
    <v-chip filter color="sent" :value="status.SENT">Versendet</v-chip>
    <v-chip filter color="payed" :value="status.PAYED">Bezahlt</v-chip>
    <v-chip filter color="archived" :value="status.ARCHIVED">Archiviert</v-chip>
  </v-chip-group>
</template>

<script>
import status from '@/components/invoice/status'

export default {
  props: {
    value: {
      type: Array,
      default: () => [status.CREATED],
    },
  },
  data() {
    return {
      status,
    }
  },
  computed: {
    filter: {
      get() {
        return this.value
      },
      set(filter) {
        this.$emit('input', filter)
      },
    },
  },
}
</script>
