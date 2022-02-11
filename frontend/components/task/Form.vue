<template>
  <Form
    :cancel="cancel"
    :save="save"
    :errors.sync="errors"
    :deleteable="isEditMode"
    :destroy="destroy"
    @success="success"
    @successDestroy="successDestroy"
    @serverError="error"
  >
    <v-col cols="12">
      <FieldsText
        :value="task.title"
        autofocus
        label="Titel"
        :rules="[validators.required('Titel')]"
        :error-messages="errors['title']"
        @input="(title) => update('title', title)"
      />
      <CustomerSelect
        :value="task.customer_id"
        :rules="[validators.required('Kunde')]"
        :error-messages="errors['customer']"
        @input="(customerId) => update('customer_id', customerId)"
      />
      <FieldsDateTime
        v-model="dtstart"
        label="Startdatum"
        :rules="[validators.required('Datum')]"
        :error-messages="errors['start']"
      />
      <FieldsDuration
        :value="task.duration"
        label="Dauer"
        :error-messages="errors['duration']"
        class="task-duration-field"
        @input="(duration) => update('duration', duration)"
      />
      <v-radio-group
        v-model="frequencyMode"
        :label="`Wiederholen (${rruleText})`"
        :error-messages="errors['frequency']"
      >
        <v-radio :value="frequencyModes.DAILY" label="Täglich" />
        <v-radio :value="frequencyModes.WEEKLY" label="Wöchentlich" />
        <v-radio :value="frequencyModes.FORT_NIGHTLY" label="Alle zwei Wochen" />
        <v-radio :value="frequencyModes.MONTHLY" label="Monatlich" />
        <TaskCustomRRuleDialog v-model="rruleDialog" :rrule-set.sync="rruleSet">
          <template #activator="{ on, attrs }">
            <v-radio v-bind="attrs" :value="frequencyModes.CUSTOM" label="Benutzerdefiniert" v-on="on" />
          </template>
        </TaskCustomRRuleDialog>
      </v-radio-group>
    </v-col>
    <TaskDeleteDialog v-model="deleteDialog" :current-date="currentDate" :task="task" @deleted="confirmDestroy" />
  </Form>
</template>

<script>
import first from 'lodash/first'
import DateTime from 'luxon/src/datetime'
import { rrulestr, RRule } from 'rrule'
import { update } from '@/rrule-helpers'

const frequencyModes = {
  DAILY: 'daily',
  WEEKLY: 'weekly',
  FORT_NIGHTLY: 'fort_nightly',
  MONTHLY: 'monthly',
  CUSTOM: 'custom',
}

export default {
  name: 'TaskForm',
  model: {
    prop: 'task',
  },
  props: {
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
      frequencyModes,
      rruleDialog: false,
      deleteDialog: false,
      errors: {},
      isEditMode: !!this.task.id,
    }
  },
  computed: {
    rruleSet: {
      get() {
        return rrulestr(this.task.rrule, { forceset: true })
      },
      set(rruleset) {
        this.update('rrule', rruleset.toString())
      },
    },
    rrule() {
      return first(this.rruleSet.rrules())
    },
    rruleText() {
      return this.rrule.toText()
    },
    dtstart: {
      get() {
        return DateTime.fromJSDate(this.rrule.options.dtstart).toISO()
      },
      set(dtstart) {
        this.rruleset = update(this.rruleSet, { dtstart: DateTime.fromISO(dtstart).toUTC().toJSDate() })
      },
    },
    frequencyMode: {
      get() {
        const { freq, interval } = this.rrule.options
        if (freq === RRule.WEEKLY && interval === 2) {
          return frequencyModes.FORT_NIGHTLY
        }
        if (freq === RRule.WEEKLY && interval === 1) {
          return frequencyModes.WEEKLY
        }
        if (freq === RRule.MONTHLY && interval === 1) {
          return frequencyModes.MONTHLY
        }
        if (freq === RRule.DAILY && interval === 1) {
          return frequencyModes.DAILY
        }
        return frequencyModes.CUSTOM
      },
      set(frequencyMode) {
        switch (frequencyMode) {
          case frequencyModes.DAILY:
            this.rruleSet = update(this.rruleSet, { interval: 1, freq: RRule.DAILY })
            break
          case frequencyModes.WEEKLY:
            this.rruleSet = update(this.rruleSet, { interval: 1, freq: RRule.WEEKLY })
            break
          case frequencyModes.FORT_NIGHTLY:
            this.rruleSet = update(this.rruleSet, { interval: 2, freq: RRule.WEEKLY })
            break
          case frequencyModes.MONTHLY:
            this.rruleSet = update(this.rruleSet, { interval: 1, freq: RRule.MONTHLY })
            break
          case frequencyModes.CUSTOM:
            this.rruleSet = update(this.rruleSet, { interval: 1, freq: RRule.WEEKLY })
            break
        }
      },
    },
  },
  methods: {
    save() {
      if (this.isEditMode) {
        return this.$axios.$patch(`tasks/${this.task.id}/`, { ...this.task })
      }
      return this.$axios.$post('tasks/', { ...this.task })
    },
    cancel() {
      this.$router.push({ name: 'index', query: this.$route.query })
    },
    destroy() {
      this.deleteDialog = true
      return new Promise((resolve, reject) => {
        this.resolveDestroy = resolve
        this.rejectDestroy = reject
      })
    },
    async confirmDestroy(promise) {
      try {
        await promise
        this.resolveDestroy()
      } catch (error) {
        this.rejectDestroy(error)
      }
    },
    success() {
      this.notifySuccess('Auftrag wurde gespeichert')
      this.$router.push('/')
    },
    successDestroy() {
      this.notifySuccess('Auftrag wurde gelöscht')
      this.deleteDialog = false
      this.$router.push('/')
    },
    error() {
      this.deleteDialog = false
      this.$router.push('/')
    },
    update(key, value) {
      this.$emit('input', { ...this.task, [key]: value })
    },
  },
}
</script>
