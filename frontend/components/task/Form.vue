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
      <v-radio-group v-model="frequency" label="Wiederholen" :error-messages="errors['frequency']">
        <v-radio :value="frequencies.daily" label="Täglich" />
        <v-radio :value="frequencies.weekly" label="Wöchentlich" />
        <v-radio :value="frequencies.fortNightly" label="Alle zwei Wochen" />
        <v-radio :value="frequencies.monthly" label="Monatlich" />
      </v-radio-group>
    </v-col>
    <TaskDeleteDialog v-model="deleteDialog" :current-date="currentDate" :task="task" @deleted="confirmDestroy" />
  </Form>
</template>

<script>
import { RRule, rrulestr } from 'rrule'
import { update } from '@/rrule-helpers'

export default {
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
      deleteDialog: false,
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
          this.rrule = update(this.rrule, { freq: frequency })
        }
      },
    },
    dtstart: {
      get() {
        return this.rrule.rrules()[0].options.dtstart
      },
      set(dtstart) {
        this.rrule = update(this.rrule, { dtstart })
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
      this.$router.push('/')
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

<style>
.task-duration-field {
  max-width: 200px;
}
</style>
