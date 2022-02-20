<template>
  <FieldsText v-model="datetime" v-bind="$attrs" type="datetime-local" />
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  inheritAttrs: false,
  props: {
    value: {
      type: String,
      default: () => '',
    },
  },
  computed: {
    datetime: {
      get() {
        return DateTime.fromISO(this.value).toUTC().toFormat("yyyy-MM-dd'T'HH:mm")
      },
      set(datetimeString) {
        const datetime = DateTime.fromFormat(datetimeString, "yyyy-MM-dd'T'HH:mm")
        this.$emit('input', datetime.setZone('UTC', { keepLocalTime: true }).toISO())
      },
    },
  },
}
</script>
