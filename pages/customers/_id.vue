<template>
  <LayoutDefault narrow :title="customer.full_name">
    <template #prepend-actions>
      <v-btn color="transparent" to="/customers" nuxt icon>
        <v-icon color="white">{{ mdiChevronLeft }}</v-icon>
      </v-btn>
    </template>
    <template #append-actions>
      <v-btn color="transparent" nuxt :to="{ name: 'customers-edit-id', params: { id: customer.id } }" icon>
        <v-icon color="white">{{ mdiPencil }}</v-icon>
      </v-btn>
    </template>
    <v-tabs v-model="tab" fixed-tabs>
      <v-tab to="#personalien">Personalien</v-tab>
      <v-tab to="#rapporte">Rapporte</v-tab>
      <v-tab to="#pauschale">Pauschale</v-tab>
      <v-tab to="#rechnungen">Rechnungen</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <CustomerPersonalDataTabItem
        value="personalien"
        :transition="false"
        :reverse-transition="false"
        :customer="customer"
      />
      <CustomerReportsTabItem value="rapporte" :transition="false" :reverse-transition="false" />
      <CustomerFlatsTabItem :flats="flats" value="pauschale" :transition="false" :reverse-transition="false" />
      <CustomerInvoicesTabItem
        :invoices="invoices"
        :filter.sync="statusFilter"
        value="rechnungen"
        :transition="false"
        :reverse-transition="false"
        @update:filter="loadInvoices"
      >
        <AddButton :to="`/invoices/new/${customer.id}`" />
      </CustomerInvoicesTabItem>
    </v-tabs-items>
  </LayoutDefault>
</template>

<script>
import { mdiPencil, mdiChevronLeft, mdiAlarm } from '@mdi/js'
import DateTime from 'luxon/src/datetime'
import status from '@/components/invoice/status'

export default {
  name: 'ShowCustomer',
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const customer = await $http.$get(`customers/${id}/`)
    return { customer }
  },
  data() {
    return {
      tab: 'personalien',
      statusFilter: [status.CREATED],
      reports: [],
      flats: [],
      invoices: [],
      reportDate: DateTime.local().toFormat('yyyy-MM-dd'),
      mdiChevronLeft,
      mdiPencil,
      mdiAlarm,
    }
  },
  watch: {
    tab: {
      handler(tab) {
        if (tab === 'rechnungen') {
          this.loadInvoices()
        } else if (tab === 'pauschale') {
          this.loadFlats()
        }
      },
      immediate: true,
    },
  },
  methods: {
    async loadInvoices() {
      const searchParams = this.statusFilter.map((status) => ['status', status])
      this.invoices = await this.$http.$get(`customers/${this.customer.id}/invoices/`, {
        searchParams,
      })
    },
    async loadFlats() {
      this.flats = await this.$http.$get(`customers/${this.customer.id}/flats/`)
    },
  },
}
</script>
