<template>
  <LayoutDefault title="Rapport" narrow>
    <v-tabs v-model="tab" fixed-tabs class="mb-4" height="40">
      <v-tab to="#rapport"> Rapport </v-tab>
      <v-tab to="#pauschal"> Pauschal </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item value="rapport">
        <Form :cancel="cancel" :save="saveReport" :errors.sync="reportErrors" @success="successReport">
          <v-col cols="12">
            <CustomerSelect v-model="report.customer_id" :error-messages="reportErrors.customer_id" />
          </v-col>
          <v-col cols="12">
            <FieldsText
              v-model="report.title"
              autofocus
              label="Titel"
              :rules="[validators.required('Titel')]"
              :error-messages="reportErrors.title"
            />
          </v-col>
          <v-col cols="4">
            <FieldsText
              v-model="report.start"
              type="datetime-local"
              label="Startzeit"
              :error-messages="reportErrors.start"
            />
          </v-col>
          <v-col cols="4">
            <FieldsText
              v-model="report.end"
              type="datetime-local"
              label="Endzeit"
              :rules="endRules"
              :error-messages="reportErrors.end"
            />
          </v-col>
          <v-col cols="4">
            <FieldsText label="Dauer" :value="reportDuration" readonly disabled />
          </v-col>
          <v-col cols="12">
            <v-checkbox v-model="report.route_flat" label="Wegpauschale" :error-messages="reportErrors.route_flat" />
          </v-col>
        </Form>
      </v-tab-item>
      <v-tab-item value="pauschal">
        <v-container>
          <Form :cancel="cancel" :save="saveFlat" :errors.sync="flatErrors" @success="successFlat">
            <v-col cols="12">
              <CustomerSelect v-model="flat.customer_id" :error-messages="flatErrors.customer_id" />
            </v-col>
            <v-col cols="12">
              <FlatTemplateSelect @input="applyTemplate" />
            </v-col>
            <v-col cols="6">
              <FieldsText
                v-model="flat.name"
                :rules="[validators.required('Name')]"
                :error-messages="flatErrors.name"
                label="Name"
              />
            </v-col>
            <v-col cols="6">
              <FieldsText
                v-model="flat.price"
                :rules="[validators.required('Preis')]"
                :error-messages="flatErrors.price"
                label="Preis"
                type="number"
                suffix="CHF"
              />
            </v-col>
          </Form>
        </v-container>
      </v-tab-item>
    </v-tabs-items>
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import get from 'lodash/get'
import { mdiChevronLeft, mdiCheck } from '@mdi/js'
import omit from 'lodash/omit'
import { mapActions } from 'vuex'

export default {
  layout: 'blank',
  async asyncData({ $http }) {
    const { customer, next_event_title: nextEventTitle } = await $http.$get('/tasks/next_event/')
    const report = (await $http.$get('/reports/running/')) || {}
    return {
      report: Object.assign({
        id: report.id || null,
        customer_id: get(report, 'customer.id', customer),
        start: report.start
          ? DateTime.fromISO(report.start).toFormat("yyyy-MM-dd'T'HH:mm")
          : DateTime.local().toFormat("yyyy-MM-dd'T'HH:mm"),
        title: report.title || nextEventTitle,
        end: report.start ? DateTime.local().toFormat("yyyy-MM-dd'T'HH:mm") : null,
        route_flat: true,
      }),
      hasRunningReport: !!report,
      flat: {
        customer_id: customer,
        name: '',
        price: 0,
      },
    }
  },
  data() {
    return {
      tab: null,
      reportErrors: {},
      flatErrors: {},
      valid: null,
      mdiChevronLeft,
      mdiCheck,
    }
  },
  computed: {
    reportDuration() {
      const start = DateTime.fromISO(this.report.start)
      if (this.report.end) {
        const end = DateTime.fromISO(this.report.end)
        return end.diff(start).toFormat('hh:mm')
      }
      return DateTime.local().diff(start).toFormat('hh:mm')
    },
    endRules() {
      return this.report.id ? [this.validators.required('Endzeit')] : []
    },
  },
  methods: {
    ...mapActions('report', ['trackReportDuration']),
    successReport() {
      this.trackReportDuration()
      this.notifySuccess('Rapport gespeichert')
      this.$router.push(`/customers/${this.report.customer_id}#rapporte`)
    },
    cancel() {
      if (this.tab === 'rapport') {
        this.$router.push(`/customers/${this.report.customer_id}#rapporte`)
      } else if (this.tab === 'pauschal') {
        this.$router.push(`/customers/${this.report.customer_id}#pauschale`)
      }
    },
    saveReport() {
      if (this.report.id) {
        return this.$http.$patch(`/reports/${this.report.id}/`, this.report)
      } else {
        return this.$http.$post(`/reports/`, this.report)
      }
    },
    successFlat() {
      this.notifySuccess('Pauschaleintrag gespeichert')
      this.$router.push(`/customers/${this.report.customer_id}#pauschale`)
    },
    saveFlat() {
      return this.$http.$post(`/flats/`, this.flat)
    },
    applyTemplate(template) {
      Object.assign(this.flat, omit(template, ['id']))
    },
  },
}
</script>
