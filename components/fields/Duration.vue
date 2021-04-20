<template>
  <v-input v-bind="$attrs" class="duration-field">
    <div class="d-flex align-center mt-1">
      <FieldsNumberStepper v-model="hours" label="Stunden" />
      <span class="title px-4">:</span>
      <FieldsNumberStepper v-model="minutes" label="Minuten" :steps="5" />
    </div>
    <template v-for="(_, name) in $scopedSlots" :slot="name" slot-scope="slotData"
      ><slot :name="name" v-bind="slotData"
    /></template>
  </v-input>
</template>

<script>
import padStart from 'lodash/padStart'

function getDurationPart(duration, part) {
  return Number.parseInt(duration.split(/:/)[part])
}

function toDurationPart(part) {
  return padStart(part, 2, '0')
}

export default {
  name: 'Duration',
  inheritAttrs: false,
  props: {
    value: {
      type: String,
      default: () => '00:00:00',
      validator(value) {
        return /\d\d:\d\d:\d\d/.test(value)
      },
    },
  },
  computed: {
    hours: {
      get() {
        return getDurationPart(this.value, 0)
      },
      set(hours) {
        this.$emit('input', this.toDurationString(hours, this.minutes, this.seconds))
      },
    },
    minutes: {
      get() {
        return getDurationPart(this.value, 1)
      },
      set(minutes) {
        this.$emit('input', this.toDurationString(this.hours, minutes, this.seconds))
      },
    },
  },
  methods: {
    toDurationString(hours, minutes) {
      return `${toDurationPart(hours)}:${toDurationPart(minutes)}:00`
    },
  },
}
</script>
<style>
.duration-field .v-input__slot {
  flex-direction: column;
  align-items: flex-start;
}
</style>
