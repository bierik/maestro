<template>
  <FieldsText v-model="datetime" v-mask="'##.##.####, ##:##'" v-bind="$attrs" :rules="[validators.datetime]" />
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  props: {
    value: {
      type: Date,
      required: true,
    },
  },
  data() {
    return {
      datetime: DateTime.fromJSDate(this.value).toUTC().toFormat('dd.MM.yyyy, HH:mm'),
    }
  },
  watch: {
    datetime(string) {
      const datetime = DateTime.fromFormat(string, 'dd.MM.yyyy, HH:mm')
      if (datetime.isValid) {
        this.$emit('input', datetime.setZone('utc', { keepLocalTime: true }).toJSDate())
      }
    },
  },
}
</script>
