<template>
  <v-tab-item v-bind="$attrs">
    <InvoiceFilter v-model="invoiceFilter" :show.sync="showFilter" />
    <ServerSideIterator :fetch="fetchInvoices" :filter="invoiceFilter">
      <template v-if="$vuetify.breakpoint.smAndDown" #append-header>
        <v-btn depressed small @click="showFilter = !showFilter"
          ><v-icon small>{{ mdiFilterOutline }}</v-icon></v-btn
        >
      </template>
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
import { mdiFilePdfBox, mdiFilterOutline } from '@mdi/js'
import flatten from 'lodash/flatten'
import isEmpty from 'lodash/isEmpty'
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
    const userStatusFilter = flatten([this.$route.query.status]).filter(Boolean)
    return {
      showFilter: this.$vuetify.breakpoint.smAndUp,
      mdiFilePdfBox,
      mdiFilterOutline,
      invoiceFilter: { status: isEmpty(userStatusFilter) ? [status.CREATED] : userStatusFilter },
    }
  },
  methods: {
    fetchInvoices({ page, itemsPerPage, filter }) {
      const params = {
        page_size: itemsPerPage,
        page,
        ...filter,
      }
      return this.$axios.$get(path.join('customers', this.$route.params.id, 'invoices/'), { params })
    },
  },
}
</script>
