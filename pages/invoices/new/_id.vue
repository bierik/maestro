<template>
  <LayoutDefault>
    <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
      <v-col cols="12">
        <CustomerSelect v-model="invoice.customer" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="invoice.start" type="date" label="Von" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="invoice.end" type="date" label="Bis" />
      </v-col>
      <template #prepend-actions>
        <InvoicePreviewDialog :src="previewURL">
          <template #activator="{ on, attrs }">
            <v-btn depressed color="primary" v-bind="attrs" v-on="on">Vorschau anzeigen</v-btn>
          </template>
        </InvoicePreviewDialog>
      </template>
    </Form>
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      invoice: {
        customer: Number.parseInt(this.$route.params.id, 10),
        start: DateTime.local().set({ day: 15 }).minus({ months: 1 }).toFormat('yyyy-MM-dd'),
        end: DateTime.local().set({ day: 15 }).toFormat('yyyy-MM-dd'),
      },
      errors: {},
    }
  },
  computed: {
    previewURL() {
      const searchParams = new URLSearchParams({
        customer: this.invoice.customer,
        start: this.invoice.start,
        end: this.invoice.end,
      })
      return `${location.origin}/api/invoices/preview/?${searchParams.toString()}`
    },
  },
  methods: {
    save() {
      return this.$axios.post('/invoices/', this.invoice)
    },
    cancel() {
      if (this.invoice.customer) {
        this.$router.push(`/customers/${this.invoice.customer}#rechnungen`)
      } else {
        this.$router.push('/invoices')
      }
    },
    success() {
      this.notifySuccess('Rechnung erstellt')
      this.$router.push(`/customers/${this.invoice.customer}#rechnungen`)
    },
  },
  head() {
    return {
      title: 'Neue Rechung',
    }
  },
}
</script>
