<template>
  <LayoutDefault title="Rechnungen" narrow>
    <InvoiceStatusFilter v-model="invoiceFilter.status" class="px-2" />
    <ServerSideIterator :fetch="fetchInvoices" :filter="invoiceFilter">
      <template #default="{ items }">
        <ListDivided :items="items">
          <template #item="{ item: invoice }">
            <v-list-item :key="`invoice-${invoice.id}`" :to="`/invoices/${invoice.id}`">
              <v-list-item-avatar>
                <v-icon color="grey--darken-2">{{ mdiFilePdfBox }}</v-icon>
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
          </template>
        </ListDivided>
      </template>
    </ServerSideIterator>
  </LayoutDefault>
</template>

<script>
import { mdiFilePdfBox } from '@mdi/js'
import status from '@/components/invoice/status'

export default {
  data() {
    return {
      invoiceFilter: { status: [status.CREATED] },
      mdiFilePdfBox,
    }
  },
  methods: {
    fetchInvoices({ page, itemsPerPage, filter }) {
      const searchParams = {
        page_size: itemsPerPage,
        page,
        ...filter,
      }
      return this.$axios.$get('invoices/', { searchParams })
    },
  },
  head() {
    return {
      title: 'Rechnungen',
    }
  },
}
</script>
