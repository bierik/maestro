<template>
  <LayoutDefault narrow title="Rechnungen">
    <v-container>
      <InvoiceFilter v-model="statusFilter" @input="loadInvoices" />
    </v-container>
    <v-list>
      <v-list-item v-for="invoice in invoices" :key="`invoice-${invoice.id}`" :to="`/invoices/${invoice.id}`">
        <v-list-item-avatar>
          <v-icon color="grey--darken-2">{{ mdiFilePdf }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="d-flex align-center">
            {{ invoice.number }}
            <InvoiceStatusChip :invoice="invoice" class="ml-2" />
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ invoice.date | dateString }}
          </v-list-item-subtitle>
          <v-list-item-subtitle>
            {{ invoice.customer.full_name }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </LayoutDefault>
</template>

<script>
import { mdiFilePdf } from '@mdi/js'
import status from '@/components/invoice/status'

export default {
  fetch() {
    this.loadInvoices()
  },
  data() {
    return {
      invoices: [],
      statusFilter: [status.CREATED],
      mdiFilePdf,
    }
  },
  methods: {
    async loadInvoices() {
      const searchParams = this.statusFilter.map((status) => ['status', status])
      this.invoices = await this.$http.$get('invoices/', {
        searchParams,
      })
    },
  },
}
</script>
