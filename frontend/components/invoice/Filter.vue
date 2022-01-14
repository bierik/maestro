<template>
  <v-navigation-drawer right absolute bottom permanent>
    <div class="d-flex flex-column">
      <FieldsText v-model="filter.number" class="mb-2" hide-details label="Nummer" />
      <CustomerSelect v-if="customerFilter" v-model="filter.customer" class="mb-2" hide-details clearable />
      <FieldsDate v-model="filter.date_after" block class="mb-2" hide-details label="Datum von" clearable />
      <FieldsDate v-model="filter.date_before" block hide-details label="Datum bis" clearable class="mb-2" />
      <InvoiceStatusFilter v-model="filter.status" />
    </div>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'InvoiceFilter',
  props: {
    value: {
      type: Object,
      required: true,
    },
    customerFilter: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    filter: {
      get() {
        return this.value
      },
      set(filter) {
        this.$emit('input', filter)
      },
    },
  },
}
</script>
