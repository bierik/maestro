<template>
  <div class="d-flex flex-column">
    <v-btn small outlined tile :disabled="!canIncrease" @click="increase"
      ><v-icon>{{ mdiChevronUp }}</v-icon></v-btn
    >
    <v-text-field v-model="number" hide-details outlined dense class="rounded-0 my-2" :label="label" />
    <v-btn small outlined tile :disabled="!canDecrease" @click="decrease"
      ><v-icon>{{ mdiChevronDown }}</v-icon></v-btn
    >
  </div>
</template>

<script>
import { mdiChevronUp, mdiChevronDown } from '@mdi/js'

export default {
  name: 'NumberStepper',
  props: {
    value: {
      type: Number,
      default: () => 0,
    },
    steps: {
      type: Number,
      default: () => 1,
    },
    label: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      mdiChevronUp,
      mdiChevronDown,
    }
  },
  computed: {
    number: {
      get() {
        return this.value || '0'
      },
      set(number) {
        if (!number) return
        this.$emit('input', number)
      },
    },
    canIncrease() {
      return this.value + this.steps < 99
    },
    canDecrease() {
      return this.value > 0
    },
  },
  methods: {
    increase() {
      const nextStep = this.number + this.steps
      if (nextStep <= 99) {
        this.$emit('input', nextStep)
      }
    },
    decrease() {
      this.$emit('input', Math.max(this.number - this.steps, 0))
    },
  },
}
</script>
