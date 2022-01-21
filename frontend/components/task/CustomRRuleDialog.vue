<template>
  <v-dialog v-model="open" max-width="600px" :fullscreen="$vuetify.breakpoint.smAndDown" v-bind="$attrs">
    <v-card tile>
      <v-card-title> Benutzerdefinierte Wiederholung </v-card-title>
      <v-card-text>
        <v-form>
          <div class="d-flex align-center mb-4">
            <strong class="mr-2 text-no-wrap">Wiederholen alle</strong>
            <FieldsText v-model="interval" style="width: 60px" dense class="mr-2 shrink" type="number" hide-details />
            <FieldsSelect
              v-model="frequency"
              dense
              :items="frequencyChoices"
              style="width: 120px"
              class="shrink"
              hide-details
            />
          </div>
          <div class="d-flex flex-column">
            <strong>Ende</strong>
            <v-radio-group v-model="untilMode">
              <v-radio label="Nie" :value="untilModes.NEVER" />
              <v-radio label="Am" :value="untilModes.AT">
                <template #label>
                  <div class="d-flex align-center">
                    <span class="mr-2">Am</span>
                    <FieldsDate
                      v-model="until"
                      dense
                      :disabled="untilMode !== untilModes.AT"
                      :rules="[validators.afterToday]"
                    />
                  </div>
                </template>
              </v-radio>
              <v-radio :value="untilModes.AFTER">
                <template #label>
                  <div class="d-flex align-center">
                    <span class="mr-2">Nach</span>
                    <FieldsText
                      v-model="count"
                      style="width: 140px"
                      dense
                      hide-details
                      type="number"
                      suffix="Terminen"
                      :disabled="untilMode !== untilModes.AFTER"
                    />
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </div>
        </v-form>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn depressed color="error" @click="cancel">Abbrechen</v-btn>
        <v-btn depressed color="success" @click="apply">Speichern</v-btn>
      </v-card-actions>
    </v-card>
    <template #activator="props">
      <slot name="activator" v-bind="props" />
    </template>
  </v-dialog>
</template>

<script>
import first from 'lodash/first'
import DateTime from 'luxon/src/datetime'
import { RRule } from 'rrule'
import { update } from '@/rrule-helpers'

const untilModes = {
  AT: 'AT',
  AFTER: 'AFTER',
  NEVER: 'NEVER',
}

const frequencyChoices = [
  { text: 'Tage', value: RRule.DAILY },
  { text: 'Wochen', value: RRule.WEEKLY },
  { text: 'Monate', value: RRule.MONTHLY },
  { text: 'Jahre', value: RRule.YEARLY },
]

export default {
  name: 'CustomRRuleDialog',
  props: {
    value: {
      type: Boolean,
      default: () => false,
    },
    rruleSet: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      intermediateRruleSet: this.rruleSet,
      untilMode: untilModes.NEVER,
      frequencyChoices,
      untilModes,
    }
  },
  computed: {
    rrule() {
      return first(this.intermediateRruleSet.rrules())
    },
    frequency: {
      get() {
        return this.rrule.options.freq
      },
      set(frequency) {
        this.intermediateRruleSet = update(this.intermediateRruleSet, { freq: frequency })
      },
    },
    interval: {
      get() {
        return this.rrule.options.interval
      },
      set(interval) {
        this.intermediateRruleSet = update(this.intermediateRruleSet, { interval })
      },
    },
    until: {
      get() {
        return (
          DateTime.fromJSDate(this.rrule.options.until).toISODate() || DateTime.utc().plus({ years: 5 }).toISODate()
        )
      },
      set(until) {
        const untilDateTime = DateTime.fromISO(until)
        const afterToday = untilDateTime > DateTime.now().startOf('day').toUTC()
        if (afterToday) {
          this.intermediateRruleSet = update(this.intermediateRruleSet, {
            until: untilDateTime.endOf('day').toUTC().toJSDate(),
          })
        }
      },
    },
    count: {
      get() {
        return this.rrule.options.count || 13
      },
      set(count) {
        this.intermediateRruleSet = update(this.intermediateRruleSet, { count })
      },
    },
    open: {
      get() {
        return this.value
      },
      set(open) {
        this.$emit('input', open)
      },
    },
  },
  watch: {
    rruleSet(rruleSet) {
      this.intermediateRruleSet = rruleSet
    },
  },
  methods: {
    apply() {
      this.$emit('update:rruleSet', this.intermediateRruleSet)
      this.open = false
    },
    cancel() {
      this.open = false
    },
  },
}
</script>
<style>
.v-input--selection-controls__input input[type='radio'] {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
  user-select: none;
}
</style>
