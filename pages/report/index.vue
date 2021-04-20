<template>
  <LayoutDefault title="Rapport">
    <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
      <v-col cols="12">
        <CustomerSelect v-model="report.customer_id" :error-messages="errors.customer_id" />
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="report.title"
          autofocus
          label="Titel"
          :rules="[validators.required('Titel')]"
          :error-messages="errors.title"
        />
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="report.start" type="datetime-local" label="Startzeit" :error-messages="errors.start" />
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="report.end"
          type="datetime-local"
          label="Endzeit"
          :rules="endRules"
          :error-messages="errors.end"
        />
      </v-col>
      <v-col cols="12">
        <v-text-field label="Dauer" :value="reportDuration" readonly disabled />
      </v-col>
    </Form>
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import get from 'lodash/get'
import { mdiChevronLeft, mdiCheck } from '@mdi/js'

export default {
  layout: 'blank',
  async asyncData({ $http }) {
    const { customer } = await $http.$get('/tasks/next_event/')
    const report = (await $http.$get('/reports/running/')) || {}
    return {
      report: Object.assign({
        id: report.id || null,
        customer_id: get(report, 'customer.id', customer),
        start: report.start
          ? DateTime.fromISO(report.start).toFormat("yyyy-MM-dd'T'HH:mm")
          : DateTime.local().toFormat("yyyy-MM-dd'T'HH:mm"),
        title: report.title || '',
        end: report.start ? DateTime.local().toFormat("yyyy-MM-dd'T'HH:mm") : null,
      }),
      hasRunningReport: !!report,
    }
  },
  data() {
    return {
      report: {},
      errors: {},
      hasRunningReport: false,
      valid: null,
      mdiChevronLeft,
      mdiCheck,
    }
  },
  computed: {
    reportDuration() {
      const start = DateTime.fromISO(this.report.start)
      return DateTime.local().diff(start).toFormat('hh:mm')
    },
    endRules() {
      return this.report.id ? [this.validators.required('Endzeit')] : []
    },
  },
  methods: {
    success() {
      this.$router.push('/')
    },
    cancel() {
      this.$router.push('/')
    },
    save() {
      if (this.report.end) {
        return this.$http.$patch(`/reports/${this.report.id}/`, this.report)
      }
      return this.$http.$post(`/reports/`, this.report)
    },
  },
}
</script>
