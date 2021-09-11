<template>
  <v-tab-item v-bind="$attrs">
    <v-container class="px-0">
      <InvoiceStatusFilter v-model="invoiceFilter.status" />
    </v-container>
    <ServerSideIterator :fetch="fetchInvoices" :filter="invoiceFilter">
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
              <v-list-item-subtitle> Erstellt am: {{ invoice.created | dateTimeString }} </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </template>
    </ServerSideIterator>
    <slot />
  </v-tab-item>
</template>

<script>
import path from 'path'
import { mdiFilePdf } from '@mdi/js'
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
      mdiFilePdf,
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
      return this.$http.$get(path.join('customers', this.$route.params.id, 'invoices'), { searchParams })
    },
  },
}
</script>
