<template>
  <v-btn v-bind="$attrs" color="primary" fab dark :small="$vuetify.breakpoint.xs" right fixed bottom class="mb-14">
    <v-icon>{{ mdiPlus }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiPlus } from '@mdi/js'

export default {
  inheritAttrs: false,
  data() {
    return {
      mdiPlus,
    }
  },
}
</script>
