<template>
  <Form
    :cancel="cancel"
    :save="save"
    :errors.sync="errors"
    lazy-validation
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
      <v-radio-group v-model="frequencyMode" label="Wiederholen" :error-messages="errors['frequency']">
        <v-radio value="daily" label="Täglich" />
        <v-radio value="weekly" label="Wöchentlich" />
        <v-radio value="fortNightly" label="Alle zwei Wochen" />
        <v-radio value="monthly" label="Monatlich" />
        <TaskCustomRRuleDialog v-model="rruleDialog" :rrule.sync="rrule" @cancel="resetRRule">
          <template #activator="{ on, attrs }">
            <v-radio v-bind="attrs" value="custom" label="Benutzerdefiniert" v-on="on" />
          </template>
        </TaskCustomRRuleDialog>
      </v-radio-group>
    </v-col>
    <TaskDeleteDialog v-model="deleteDialog" :current-date="currentDate" :task="task" @deleted="confirmDestroy" />
  </Form>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import { RRule, rrulestr } from 'rrule'
import { update } from '@/rrule-helpers'

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
      originalRRule: this.task.rrule,
      rruleDialog: false,
      deleteDialog: false,
      frequencyMode: 'weekly',
      frequencies: {
        daily: RRule.DAILY,
        weekly: RRule.WEEKLY,
        fortNightly: 'FORT_NIGHTLY',
        monthly: RRule.MONTHLY,
      },
      errors: {},
      isEditMode: !!this.task.id,
    }
  },
  computed: {
    rrule: {
      get() {
        return rrulestr(this.task.rrule, { forceset: true })
      },
      set(rrule) {
        this.update('rrule', rrule.toString())
      },
    },
    frequency: {
      get() {
        if (this.rrule.rrules()[0].options.interval === 2 && this.rrule.rrules()[0].options.freq === RRule.WEEKLY) {
          return this.frequencies.fortNightly
        }
        return this.rrule.rrules()[0].options.freq
      },
      set(frequency) {
        if (frequency === this.frequencies.fortNightly) {
          this.rrule = update(this.rrule, { freq: RRule.WEEKLY, interval: 2 })
        } else {
          this.rrule = update(this.rrule, { freq: frequency, interval: 1 })
        }
      },
    },
    dtstart: {
      get() {
        return DateTime.fromJSDate(this.rrule.rrules()[0].options.dtstart).toISO()
      },
      set(dtstart) {
        this.rrule = update(this.rrule, { dtstart: DateTime.fromISO(dtstart).toUTC().toJSDate() })
      },
    },
  },
  watch: {
    frequencyMode(frequencyMode) {
      if (frequencyMode === 'custom') {
        this.frequency = RRule.WEEKLY
        this.rruleDialog = true
      } else {
        this.frequency = this.frequencies[frequencyMode]
      }
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
      this.$router.push('/')
    },
    destroy() {
      this.deleteDialog = true
      return new Promise((resolve, reject) => {
        this.resolveDestroy = resolve
        this.rejectDestroy = reject
      })
    },
    resetRRule() {
      this.update('rrule', this.originalRRule)
      this.frequencyMode = 'weekly'
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
