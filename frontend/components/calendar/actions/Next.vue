<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="next()">
    <v-icon>{{ mdiChevronRight }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiChevronRight } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  inheritAttrs: false,
  data() {
    return {
      mdiChevronRight,
    }
  },
  methods: {
    ...mapActions('calendar', ['next']),
  },
}
</script>
