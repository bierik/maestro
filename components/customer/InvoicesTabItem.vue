<template>
  <v-tab-item v-bind="$attrs">
    <v-container>
      <InvoiceFilter v-model="statusFilter" />
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
          <v-list-item-subtitle> Erstellt am: {{ invoice.created | dateTimeString }} </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <slot />
  </v-tab-item>
</template>

<script>
import { mdiFilePdf } from '@mdi/js'

export default {
  inheritAttrs: false,
  props: {
    invoices: {
      type: Array,
      default: () => [],
    },
    filter: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      mdiFilePdf,
    }
  },
  computed: {
    statusFilter: {
      get() {
        return this.filter
      },
      set(filter) {
        this.$emit('update:filter', filter)
      },
    },
  },
}
</script>
