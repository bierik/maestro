<template>
  <v-dialog v-model="show" v-bind="$attrs" max-width="600px" :fullscreen="$vuetify.breakpoint.smAndDown">
    <v-card tile>
      <v-card-title>Wiederkehrender Termin löschen</v-card-title>
      <v-card-text>
        <v-radio-group v-model="deleteOption">
          <v-radio label="Diesen Termin" :value="deleteOptions.THIS_EVENT" />
          <v-radio label="Diesen Termin und alle folgenden" :value="deleteOptions.THIS_AND_FOLLOWING_EVENTS" />
          <v-radio label="Alle Termine" :value="deleteOptions.ALL_EVENTS" />
        </v-radio-group>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn depressed color="error" @click="show = false">Abbrechen</v-btn>
        <v-btn depressed color="error" @click="destroy">Löschen</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { rrulestr } from 'rrule'
import DateTime from 'luxon/src/datetime'
import { exclude, until } from '@/rrule-helpers'

const deleteOptions = {
  THIS_EVENT: 1,
  THIS_AND_FOLLOWING_EVENTS: 2,
  ALL_EVENTS: 3,
}

export default {
  props: {
    value: {
      type: Boolean,
      default: () => false,
    },
    task: {
      type: Object,
      required: true,
    },
    currentDate: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      deleteOptions,
      deleteOption: deleteOptions.THIS_EVENT,
    }
  },
  computed: {
    show: {
      get() {
        return this.value
      },
      set(show) {
        this.$emit('input', show)
      },
    },
  },
  methods: {
    destroy() {
      const rruleset = rrulestr(this.task.rrule, { forceset: true })

      switch (this.deleteOption) {
        case deleteOptions.THIS_EVENT:
          this.$emit(
            'deleted',
            this.$axios.$patch(`tasks/${this.task.id}/`, {
              rrule: exclude(rruleset, DateTime.fromISO(this.currentDate).toJSDate()).toString(),
            }),
          )
          break
        case deleteOptions.THIS_AND_FOLLOWING_EVENTS:
          this.$emit(
            'deleted',
            this.$axios.$patch(`tasks/${this.task.id}/`, {
              rrule: until(rruleset, DateTime.fromISO(this.currentDate).toJSDate()).toString(),
            }),
          )
          break
        default:
          this.$emit('deleted', this.$axios.$delete(`tasks/${this.task.id}/`))
      }
    },
  },
}
</script>
