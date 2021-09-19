<template>
  <LayoutDefault title="Rapport">
    <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
      <v-col cols="12">
        <CustomerSelect v-model="report.customer_id" :error-messages="errors.customer_id" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="report.title" label="Titel" :error-messages="errors.title" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="report.start" type="datetime-local" label="Startzeit" :error-messages="errors.start" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="report.end" type="datetime-local" label="Endzeit" :error-messages="errors.end" />
      </v-col>
      <v-col cols="12">
        <v-checkbox v-model="report.route_flat" label="Wegpauschale" :error-messages="errors.route_flat" />
      </v-col>
      <v-col cols="12">
        <FieldsText readonly disabled :value="duration" />
      </v-col>
    </Form>
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  async asyncData({
    $axios,
    route: {
      params: { id },
    },
  }) {
    const report = await $axios.$get(`reports/${id}/`)
    return {
      report: {
        id: report.id,
        start: DateTime.fromISO(report.start).toFormat("yyyy-MM-dd'T'HH:mm"),
        end: DateTime.fromISO(report.end).toFormat("yyyy-MM-dd'T'HH:mm"),
        title: report.title,
        customer_id: report.customer.id,
        route_flat: report.route_flat,
      },
    }
  },
  data() {
    return {
      errors: {},
    }
  },
  computed: {
    duration() {
      const start = DateTime.fromISO(this.report.start)
      const end = DateTime.fromISO(this.report.end)
      return end.diff(start).toFormat('hh:mm')
    },
  },
  methods: {
    save() {
      return this.$axios.$patch(`reports/${this.report.id}/`, this.report)
    },
    cancel() {
      this.$router.push(`/customers/${this.report.customer_id}#rapporte`)
    },
    success() {
      this.notifySuccess('Rapport wurde aktualisiert')
      this.$router.push(`/customers/${this.report.customer_id}#rapporte`)
    },
  },
}
</script>
