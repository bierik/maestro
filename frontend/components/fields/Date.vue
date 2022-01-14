<template>
  <FieldsText v-model="date" v-bind="$attrs" type="date" :style="block ? '' : 'width: 190px'" />
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  name: 'DateField',
  inheritAttrs: false,
  props: {
    value: {
      type: String,
      default: '',
    },
    block: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    date: {
      get() {
        return this.value
      },
      set(dateString) {
        const date = DateTime.fromISO(dateString)
        if (date.isValid) {
          this.$emit('input', date.toISODate())
        }
      },
    },
  },
}
</script>
