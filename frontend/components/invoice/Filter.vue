<template>
  <v-navigation-drawer
    app
    right
    stateless
    :temporary="$vuetify.breakpoint.smAndDown"
    :value="show"
    @input="$emit('update:show', $event)"
  >
    <h2 class="pa-2 title">Filtern</h2>
    <v-divider class="mb-2 mt-5" />
    <div class="d-flex flex-column">
      <FieldsText v-model="filter.number" class="mb-2" hide-details label="Nummer" />
      <CustomerSelect v-if="customerFilter" v-model="filter.customer" class="mb-2" hide-details clearable />
      <FieldsDate v-model="filter.date_after" block class="mb-2" hide-details label="Datum von" clearable />
      <FieldsDate v-model="filter.date_before" block hide-details label="Datum bis" clearable class="mb-2" />
      <InvoiceStatusFilter v-model="filter.status" />
    </div>
    <template v-if="$vuetify.breakpoint.smAndDown" #append>
      <v-btn fab color="primary" small class="mb-2 ml-2 elevation-0" @click="$emit('update:show', false)"
        ><v-icon>{{ mdiChevronRight }}</v-icon></v-btn
      >
    </template>
  </v-navigation-drawer>
</template>

<script>
import { mdiChevronRight } from '@mdi/js'

export default {
  name: 'InvoiceFilter',
  props: {
    show: {
      type: Boolean,
      default: () => false,
    },
    value: {
      type: Object,
      required: true,
    },
    customerFilter: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return { mdiChevronRight }
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
