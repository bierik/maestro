<template>
  <v-btn v-bind="$attrs" icon class="inherit-color" @click="prev()">
    <v-icon>{{ mdiChevronLeft }}</v-icon>
  </v-btn>
</template>

<script>
import { mdiChevronLeft } from '@mdi/js'
import { mapActions } from 'vuex'

export default {
  name: 'PrevAction',
  inheritAttrs: false,
  data() {
    return {
      mdiChevronLeft,
    }
  },
  methods: {
    ...mapActions('calendar', ['prev']),
  },
}
</script>
