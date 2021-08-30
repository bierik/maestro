<template>
  <LayoutDefault narrow title="Rechnungen">
    <ServerSideIterator :fetch="fetchInvoices" :filter="invoiceFilter">
      <template #header>
        <InvoiceStatusFilter v-model="invoiceFilter.status" />
      </template>
      <template #default="{ items }">
        <v-list>
          <v-list-item v-for="invoice in items" :key="`invoice-${invoice.id}`" :to="`/invoices/${invoice.id}`">
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
      </template>
    </ServerSideIterator>
  </LayoutDefault>
</template>

<script>
import { mdiFilePdf } from '@mdi/js'
import status from '@/components/invoice/status'

export default {
  data() {
    return {
      invoiceFilter: { status: [status.CREATED] },
      mdiFilePdf,
    }
  },
  methods: {
    fetchInvoices({ page, itemsPerPage, filter }) {
      const searchParams = {
        page_size: itemsPerPage,
        page,
        ...filter,
      }
      return this.$http.$get('invoices/', { searchParams })
    },
  },
}
</script>
