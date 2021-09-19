<template>
  <LayoutDefault :title="invoice.number">
    <template #prepend-actions>
      <v-btn icon :to="`/customers/${invoice.customer.id}#rechnungen`">
        <v-icon>{{ mdiChevronLeft }}</v-icon>
      </v-btn>
    </template>
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
      <div class="mb-4 ml-4">
        <InvoicePreviewDialog :src="invoice.url">
          <template #activator="{ on, attrs }">
            <v-btn v-bind="attrs" color="primary" depressed v-on="on">
              <v-icon left>{{ mdiFilePdfBox }}</v-icon>
              <span>Vorschau anzeigen</span>
            </v-btn>
          </template>
        </InvoicePreviewDialog>
      </div>
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
import { mdiChevronLeft, mdiCog, mdiSend, mdiCurrencyUsd, mdiArchive, mdiFilePdfBox } from '@mdi/js'
import status from '@/components/invoice/status'

export default {
  async asyncData({
    $axios,
    route: {
      params: { id },
    },
  }) {
    const invoice = await $axios.$get(`invoices/${id}/`)
    return { invoice }
  },
  data() {
    return {
      mdiChevronLeft,
      mdiCog,
      mdiSend,
      mdiCurrencyUsd,
      mdiArchive,
      mdiFilePdfBox,
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
      this.invoice = await this.$axios.$get(`invoices/${this.invoice.id}/`)
    },
    statusIcon({ status }) {
      return this.STATUS_MAPPING[status].icon
    },
    statusActions({ status }) {
      return this.STATUS_MAPPING[status].actions
    },
    async send() {
      await this.$axios.$post(`/invoices/${this.invoice.id}/send/`)
      this.reloadInvoice()
    },
    async pay() {
      await this.$axios.$post(`/invoices/${this.invoice.id}/pay/`)
      this.reloadInvoice()
    },
    async archive() {
      await this.$axios.$post(`/invoices/${this.invoice.id}/archive/`)
      this.reloadInvoice()
    },
  },
  head() {
    return {
      title: ['Rechnung', this.invoice.number].join(' - '),
    }
  },
}
</script>
