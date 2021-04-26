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
      <v-tab to="#rechnungen">Rechnungen</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item value="personalien" :transition="false" :reverse-transition="false">
        <v-list>
          <v-subheader> Personalien </v-subheader>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.last_name }}
              </v-list-item-title>
              <v-list-item-subtitle> Nachname </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.first_name }}
              </v-list-item-title>
              <v-list-item-subtitle> Vorname </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.price_per_hour }}
              </v-list-item-title>
              <v-list-item-subtitle> Stundenansatz </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-subheader> Adressen </v-subheader>
          <v-list-item v-for="address in customer.addresses" :key="`address-${address.id}`">
            <v-list-item-icon>
              <v-icon v-if="address.is_primary">{{ mdiRadioboxMarked }}</v-icon>
              <v-icon v-else>{{ mdiRadioboxBlank }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ address.address }}
              </v-list-item-title>
              <v-list-item-subtitle> {{ address.zip_code }} {{ address.place }} </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
      <v-tab-item value="rapporte" :transition="false" :reverse-transition="false">
        <v-container>
          <v-text-field
            v-model="reportDate"
            style="max-width: 200px"
            label="Datum"
            type="date"
            @input="loadReportsAndFlats"
          />
        </v-container>
        <v-list>
          <v-subheader>Rapporte</v-subheader>
          <v-list-item v-for="report in reports" :key="`report-${report.id}`" :to="`/reports/${report.id}`">
            <v-list-item-content>
              <v-list-item-title>
                {{ report.title }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ report.start | dateString }}
              </v-list-item-subtitle>
              <v-list-item-subtitle v-if="report.end">
                {{ report.start | timeString }} - {{ report.end | timeString }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action v-if="!report.end">
              <v-btn icon to="/report">
                <v-icon color="primary">{{ mdiAlarm }}</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-subheader>Pauschale</v-subheader>
          <v-list-item v-for="flat in flats" :key="`flat-${flat.id}`" :to="`/flats/${flat.id}`">
            <v-list-item-content>
              <v-list-item-title>
                {{ flat.name }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ flat.price }}
              </v-list-item-subtitle>
              <v-list-item-subtitle>
                {{ flat.created | dateTimeString }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
      <v-tab-item value="rechnungen" :transition="false" :reverse-transition="false">
        <v-container>
          <InvoiceFilter v-model="statusFilter" @input="loadInvoices" />
        </v-container>
        <v-list>
          <v-list-item v-for="invoice in invoices" :key="`invoice-${invoice.id}`" :to="`/invoices/${invoice.id}`">
            <v-list-item-avatar>
              <v-icon color="grey--darken-2">{{ mdiFilePdf }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="d-flex align-center">
                {{ invoice.number }}
                <v-chip x-small :color="statusColor(invoice)" class="ml-2">{{ invoice.status_display }}</v-chip>
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ invoice.date | dateString }}
              </v-list-item-subtitle>
              <v-list-item-subtitle> Erstellt am: {{ invoice.created | dateTimeString }} </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <AddButton :to="`/invoices/new/${customer.id}`" />
      </v-tab-item>
    </v-tabs-items>
  </LayoutDefault>
</template>

<script>
import { mdiPencil, mdiChevronLeft, mdiRadioboxMarked, mdiRadioboxBlank, mdiAlarm, mdiFilePdf } from '@mdi/js'
import DateTime from 'luxon/src/datetime'
import status, { colors } from '@/components/invoice/status'

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
      mdiRadioboxMarked,
      mdiRadioboxBlank,
      mdiAlarm,
      mdiFilePdf,
    }
  },
  watch: {
    tab: {
      handler(tab) {
        if (tab === 'rechnungen') {
          this.loadInvoices()
        } else if (tab === 'rapporte') {
          this.loadReportsAndFlats()
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
    async loadReportsAndFlats() {
      this.reports = await this.$http.$get(`customers/${this.customer.id}/reports/`, {
        searchParams: { date: this.reportDate },
      })
      this.flats = await this.$http.$get(`customers/${this.customer.id}/flats/`, {
        searchParams: { date: this.reportDate },
      })
    },
    statusColor(invoice) {
      return colors[invoice.status]
    },
  },
}
</script>
