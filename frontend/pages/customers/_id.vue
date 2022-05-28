<template>
  <LayoutDefault narrow>
    <template #title>
      <div class="d-flex align-center">
        {{ customer.full_name }}
        <v-chip v-if="!customer.is_active" class="ml-2" color="warning" small>Deaktiviert</v-chip>
      </div>
    </template>
    <template #prepend-actions>
      <v-btn color="transparent" to="/customers" nuxt icon>
        <v-icon color="white">{{ mdiChevronLeft }}</v-icon>
      </v-btn>
    </template>
    <v-tabs v-model="tab" fixed-tabs class="mb-4" height="40">
      <v-tab to="#personalien">Personalien</v-tab>
      <v-tab to="#rapporte">Rapporte</v-tab>
      <v-tab to="#pauschale">Pauschale</v-tab>
      <v-tab to="#rechnungen">Rechnungen</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab" touchless>
      <CustomerPersonalDataTabItem
        value="personalien"
        :transition="false"
        :reverse-transition="false"
        :customer="customer"
      />
      <CustomerReportsTabItem value="rapporte" :transition="false" :reverse-transition="false" />
      <CustomerFlatsTabItem value="pauschale" :transition="false" :reverse-transition="false" />
      <CustomerInvoicesTabItem value="rechnungen" :transition="false" :reverse-transition="false">
        <AddButton :to="`/invoices/new/${customer.id}`" />
      </CustomerInvoicesTabItem>
    </v-tabs-items>
  </LayoutDefault>
</template>

<script>
import { mdiPencil, mdiChevronLeft, mdiAlarm } from '@mdi/js'
import upperFirst from 'lodash/upperFirst'
import DateTime from 'luxon/src/datetime'

export default {
  name: 'ShowCustomer',
  async asyncData({
    $axios,
    route: {
      params: { id },
    },
  }) {
    const customer = await $axios.$get(`customers/${id}/`)
    return { customer }
  },
  data() {
    return {
      tab: 'personalien',
      reports: [],
      flats: [],
      invoices: [],
      reportDate: DateTime.local().toFormat('yyyy-MM-dd'),
      mdiChevronLeft,
      mdiPencil,
      mdiAlarm,
    }
  },
  head() {
    return {
      title: [upperFirst(this.tab), this.customer.full_name].join(' - '),
    }
  },
  methods: {
    async loadFlats() {
      this.flats = await this.$axios.$get(`customers/${this.customer.id}/flats/`)
    },
  },
}
</script>
