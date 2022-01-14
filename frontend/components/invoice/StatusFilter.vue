<template>
  <FieldsSelect v-model="filter" :items="filterStates" multiple label="Status" clearable />
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
      filterStates: [
        { value: status.CREATED, text: 'Erstellt' },
        { value: status.SENT, text: 'Versendet' },
        { value: status.PAYED, text: 'Bezahlt' },
        { value: status.ARCHIVED, text: 'Archiviert' },
      ],
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
