<template>
  <LayoutDefault :title="invoice.number" narrow>
    <portal to="append-actions">
      <InvoicePreviewDialog :src="invoice.url">
        <template #activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>{{ mdiFilePdf }}</v-icon>
          </v-btn>
        </template>
      </InvoicePreviewDialog>
    </portal>
    <portal to="prepend-actions">
      <v-btn icon :to="`/customers/${invoice.customer.id}#rechnungen`">
        <v-icon>{{ mdiChevronLeft }}</v-icon>
      </v-btn>
    </portal>
    <div class="d-flex flex-column fill-height grow">
      <v-list>
        <v-list-item :to="`/customers/${invoice.customer.id}`">
          <v-list-item-content>
            <v-list-item-title> Kunde </v-list-item-title>
            <v-list-item-subtitle>
              {{ invoice.customer.full_name }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Rechnungsnummer </v-list-item-title>
            <v-list-item-subtitle>
              {{ invoice.number }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title> Rechnungsdatum </v-list-item-title>
            <v-list-item-subtitle>
              {{ invoice.date | dateString }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-timeline dense clipped class="grow">
        <v-timeline-item v-for="historyEntry in invoice.history" :key="`history-entry-${historyEntry.id}`" fill-dot>
          <template v-slot:icon>
            <v-icon small color="white">{{ statusIcon(historyEntry) }}</v-icon>
          </template>
          <div class="d-flex pr-4 flex-column">
            <div class="d-flex flex-column mb-2">
              <strong>{{ historyEntry.status_display }}</strong>
              <span>{{ historyEntry.created | dateTimeString }}</span>
            </div>
            <div v-if="invoice.status === historyEntry.status">
              <v-btn
                v-for="action in statusActions(historyEntry)"
                :key="`history-entry-${historyEntry.id}-action-${action.name}`"
                depressed
                color="primary"
                @click="action.action"
              >
                {{ action.name }}
              </v-btn>
            </div>
          </div>
        </v-timeline-item>
      </v-timeline>
    </div>
  </LayoutDefault>
</template>

<script>
import { mdiChevronLeft, mdiCog, mdiSend, mdiCurrencyUsd, mdiArchive, mdiFilePdf } from '@mdi/js'
import status from '@/components/invoice/status'

export default {
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const invoice = await $http.$get(`invoices/${id}/`)
    return { invoice }
  },
  data() {
    return {
      mdiChevronLeft,
      mdiCog,
      mdiSend,
      mdiCurrencyUsd,
      mdiArchive,
      mdiFilePdf,
      STATUS_MAPPING: {
        [status.CREATED]: {
          icon: mdiCog,
          actions: [
            {
              name: 'Versendet',
              action: () => {
                this.send()
              },
            },
          ],
        },
        [status.SENT]: {
          icon: mdiSend,
          actions: [
            {
              name: 'Bezahlt',
              action: () => {
                this.pay()
              },
            },
          ],
        },
        [status.PAYED]: {
          icon: mdiCurrencyUsd,
          actions: [
            {
              name: 'Archivieren',
              action: () => {
                this.archive()
              },
            },
          ],
        },
        [status.ARCHIVED]: {
          icon: mdiArchive,
          actions: [],
        },
      },
    }
  },
  methods: {
    async reloadInvoice() {
      this.invoice = await this.$http.$get(`invoices/${this.invoice.id}/`)
    },
    statusIcon({ status }) {
      return this.STATUS_MAPPING[status].icon
    },
    statusActions({ status }) {
      return this.STATUS_MAPPING[status].actions
    },
    async send() {
      await this.$http.$post(`/invoices/${this.invoice.id}/send/`)
      this.reloadInvoice()
    },
    async pay() {
      await this.$http.$post(`/invoices/${this.invoice.id}/pay/`)
      this.reloadInvoice()
    },
    async archive() {
      await this.$http.$post(`/invoices/${this.invoice.id}/archive/`)
      this.reloadInvoice()
    },
  },
}
</script>
