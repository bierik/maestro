<template>
  <v-dialog v-model="open" max-width="600px" :fullscreen="$vuetify.breakpoint.smAndDown" v-bind="$attrs">
    <v-card tile>
      <v-card-title> Benutzerdefinierte Wiederholung </v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <div class="d-flex align-center mb-4">
            <strong class="mr-2 text-no-wrap">Wiederholen alle</strong>
            <FieldsText v-model="interval" style="width: 60px" dense class="mr-2 shrink" type="number" hide-details />
            <FieldsSelect
              v-model="frequency"
              dense
              :items="intervalUnits"
              style="width: 120px"
              class="shrink"
              hide-details
            />
          </div>
          <div class="d-flex flex-column">
            <strong>Ende</strong>
            <v-radio-group v-model="endKey">
              <v-radio label="Nie" value="NEVER" />
              <v-radio label="Am" value="AT">
                <template #label>
                  <div class="d-flex align-center">
                    <span class="mr-2">Am</span>
                    <FieldsDate
                      v-model="untilIntermediate"
                      dense
                      :disabled="endKey !== 'AT'"
                      :rules="[validators.afterToday]"
                    />
                  </div>
                </template>
              </v-radio>

              <v-radio value="AFTER">
                <template #label>
                  <div class="d-flex align-center">
                    <span class="mr-2">Nach</span>
                    <FieldsText
                      v-model="countIntermediate"
                      style="width: 140px"
                      dense
                      hide-details
                      type="number"
                      suffix="Terminen"
                      :disabled="endKey !== 'AFTER'"
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
import DateTime from 'luxon/src/datetime'
import { RRule, RRuleSet } from 'rrule'
import { update } from '@/rrule-helpers'

const defaultRRule = new RRuleSet()
defaultRRule.rrule(
  new RRule({
    interval: 1,
    freq: RRule.WEEKLY,
  }),
)

export default {
  name: 'CustomRRuleDialog',
  props: {
    value: {
      type: Boolean,
      default: () => false,
    },
    rrule: {
      type: Object,
      default: () => defaultRRule,
    },
  },
  data() {
    return {
      intermediateRRule: this.rrule,
      intervalUnits: [
        { text: 'Tage', value: RRule.DAILY },
        { text: 'Wochen', value: RRule.WEEKLY },
        { text: 'Monate', value: RRule.MONTHLY },
        { text: 'Jahre', value: RRule.YEARLY },
      ],
      endKey: 'NEVER',
      untilIntermediate: DateTime.local().plus({ years: 5 }).toISODate(),
      countIntermediate: 13,
      valid: null,
    }
  },
  computed: {
    interval: {
      get() {
        return this.intermediateRRule.rrules()[0].options.interval
      },
      set(interval) {
        this.intermediateRRule = update(this.intermediateRRule, { interval })
      },
    },
    count: {
      get() {
        return this.intermediateRRule.rrules()[0].options.count
      },
      set(count) {
        this.intermediateRRule = update(this.intermediateRRule, { count })
      },
    },
    until: {
      get() {
        return this.intermediateRRule.rrules()[0].options.until
      },
      set(until) {
        this.intermediateRRule = update(this.intermediateRRule, { until })
      },
    },
    frequency: {
      get() {
        return this.intermediateRRule.rrules()[0].options.freq
      },
      set(freq) {
        this.intermediateRRule = update(this.intermediateRRule, { freq })
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
    countIntermediate(count) {
      this.intermediateRRule = update(this.intermediateRRule, { count })
    },
    untilIntermediate(until) {
      const untilDateTime = DateTime.fromISO(until)
      const afterToday = untilDateTime > DateTime.now().startOf('day').toUTC()
      if (afterToday) {
        this.intermediateRRule = update(this.intermediateRRule, {
          until: DateTime.fromISO(until).endOf('day').toUTC().toJSDate(),
        })
      }
    },
    endKey(endKey) {
      switch (endKey) {
        case 'AT':
          this.intermediateRRule = update(this.intermediateRRule, { until: this.untilIntermediate })
          break
        case 'AFTER':
          this.intermediateRRule = update(this.intermediateRRule, { count: this.countIntermediate })
          break
        default:
          this.intermediateRRule = update(this.intermediateRRule, { until: undefined, count: undefined })
          break
      }
    },
  },
  methods: {
    apply() {
      this.$emit('update:rrule', this.intermediateRRule)
      this.open = false
    },
    cancel() {
      this.open = false
      this.$emit('cancel')
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
