<template>
  <v-tab-item v-bind="$attrs">
    <InvoiceStatusFilter v-model="invoiceFilter.status" class="px-4" />
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
                <v-list-item-subtitle> Erstellt am: {{ invoice.created | dateTimeString }} </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </ListDivided>
      </template>
    </ServerSideIterator>
    <slot />
  </v-tab-item>
</template>

<script>
import path from 'path'
import { mdiFilePdfBox } from '@mdi/js'
import flatten from 'lodash/flatten'

import status from '@/components/invoice/status'
export default {
  inheritAttrs: false,
  props: {
    filter: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      mdiFilePdfBox,
      invoiceFilter: { status: flatten([this.$route.query.status]) || [status.CREATED] },
    }
  },
  methods: {
    fetchInvoices({ page, itemsPerPage, filter }) {
      const searchParams = {
        page_size: itemsPerPage,
        page,
        ...filter,
      }
      return this.$http.$get(path.join('customers', this.$route.params.id, 'invoices/'), { searchParams })
    },
  },
}
</script>
