<template>
  <v-snackbar
    :value="show"
    :color="severityColor"
    :data-severity="severity"
    :timeout="timeout"
    data-testid="snackbar-container"
    tile
    width="100%"
    top
    app
    text
    @input="close"
  >
    <span data-testid="snackbar-message">{{ message }}</span>
    <template #action>
      <v-btn icon @click.native="close">
        <v-icon>{{ mdiClose }}</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import { mdiClose } from '@mdi/js'
import { SEVERITIES, SEVERITY_COLOR_MAPPING } from '@/store/notification'

export default {
  data() {
    return {
      mdiClose,
    }
  },
  computed: {
    ...mapState('notification', ['show', 'message', 'severity']),
    severityColor() {
      return this.$vuetify.theme.themes.light[SEVERITY_COLOR_MAPPING[this.severity]]
    },
    timeout() {
      if (this.severity === SEVERITIES.ERROR) {
        return -1
      }
      return 2000
    },
  },
  methods: {
    ...mapMutations({
      close: 'notification/close',
    }),
  },
}
</script>
<style>
.v-snack__wrapper {
  margin: 0;
}
</style>
