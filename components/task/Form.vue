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
  >
    <v-col cols="12">
      <FieldsText
        v-model="task.title"
        autofocus
        label="Titel"
        :rules="[validators.required('Titel')]"
        :error-messages="errors['title']"
      />
      <CustomerSelect
        v-model="task.customer_id"
        :rules="[validators.required('Kunde')]"
        :error-messages="errors['customer']"
      />
      <FieldsText
        v-model="dtstart"
        type="datetime-local"
        label="Startdatum"
        :rules="[validators.required('Datum')]"
        :error-messages="errors['start']"
      />
      <FieldsDuration
        v-model="task.duration"
        label="Dauer"
        :error-messages="errors['duration']"
        class="task-duration-field"
      />
      <v-radio-group v-model="frequency" label="Wiederholen" :error-messages="errors['frequency']">
        <v-radio :value="frequencies.daily" label="Täglich" />
        <v-radio :value="frequencies.weekly" label="Wöchentlich" />
        <v-radio :value="frequencies.fortNightly" label="Alle zwei Wochen" />
        <v-radio :value="frequencies.monthly" label="Monatlich" />
      </v-radio-group>
    </v-col>
  </Form>
</template>

<script>
import { rrulestr, RRule } from 'rrule'
import DateTime from 'luxon/src/datetime'

const htmlDateTimeLocalFormat = "yyyy-MM-dd'T'HH:mm"

export default {
  props: {
    task: {
      type: Object,
      default: () => ({
        duration: this.$route.query.duration || '01:00:00',
      }),
    },
  },
  data() {
    return {
      frequencies: {
        daily: RRule.DAILY,
        weekly: RRule.WEEKLY,
        fortNightly: 'FORT_NIGHTLY',
        monthly: RRule.MONTHLY,
      },
      errors: {},
      isEditMode: !!this.task.title,
      rrule: this.task.title
        ? rrulestr(this.task.rrule)
        : new RRule({
            freq: RRule.WEEKLY,
            dtstart:
              (this.$route.query.start ? DateTime.fromISO(this.$route.query.start).toJSDate() : false) || new Date(),
          }),
    }
  },
  computed: {
    frequency: {
      get() {
        if (this.rrule.options.interval === 2 && this.rrule.options.freq === RRule.WEEKLY) {
          return this.frequencies.fortNightly
        }
        return this.rrule.options.freq
      },
      set(frequency) {
        if (frequency === this.frequencies.fortNightly) {
          this.rrule = new RRule({ freq: RRule.WEEKLY, dtstart: this.rrule.options.dtstart, interval: 2 })
        } else {
          this.rrule = new RRule({ freq: frequency, dtstart: this.rrule.options.dtstart })
        }
      },
    },
    dtstart: {
      get() {
        return DateTime.fromJSDate(this.rrule.options.dtstart).toFormat(htmlDateTimeLocalFormat)
      },
      set(dtstart) {
        const dtstartDateTime = DateTime.fromFormat(dtstart, htmlDateTimeLocalFormat).toJSDate()
        this.rrule = new RRule({ freq: this.rrule.options.freq, dtstart: dtstartDateTime })
      },
    },
  },
  methods: {
    save() {
      if (this.isEditMode) {
        return this.$http.$patch(`tasks/${this.task.id}/`, { ...this.task, rrule: this.rrule.toString() })
      }
      return this.$http.$post('tasks/', { ...this.task, rrule: this.rrule.toString() })
    },
    cancel() {
      this.$router.push('/calendar')
    },
    destroy() {
      return this.$http.$delete(`tasks/${this.task.id}/`)
    },
    success() {
      this.notifySuccess('Auftrag wurde gespeichert')
      this.$router.push('/calendar')
    },
    successDestroy() {
      this.notifySuccess('Auftrag wurde gelöscht')
      this.$router.push('/calendar')
    },
  },
}
</script>

<style>
.task-duration-field {
  max-width: 200px;
}
</style>
