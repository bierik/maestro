<template>
  <FieldsText v-model="date" v-bind="$attrs" type="date" style="width: 190px" />
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  inheritAttrs: false,
  props: {
    value: {
      type: Date,
      required: true,
    },
  },
  computed: {
    date: {
      get() {
        return DateTime.fromJSDate(this.value).toISODate()
      },
      set(dateString) {
        const date = DateTime.fromISO(dateString).toUTC()
        if (date.isValid) {
          this.$emit('input', date.toJSDate())
        }
      },
    },
  },
}
</script>
