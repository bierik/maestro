<template>
  <LayoutDefault>
    <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
      <v-col cols="12">
        <CustomerSelect v-model="invoice.customer" :addresses.sync="addresses" />
      </v-col>
      <v-col cols="12">
        <FieldsSelect
          v-if="invoice.customer"
          v-model="invoice.address"
          label="Adresse"
          item-value="id"
          item-text="address"
          :items="addresses"
        >
          <template #item="{ item: address }">
            {{ address.address }}, {{ address.zip_code }} {{ address.place }}
            <v-chip v-if="address.is_primary" class="ml-2" small>Primäradresse</v-chip>
          </template>
          <template #selection="{ item: address }">
            {{ address.address }}, {{ address.zip_code }} {{ address.place }}
            <v-chip v-if="address.is_primary" class="ml-2" small>Primäradresse</v-chip>
          </template>
        </FieldsSelect>
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="invoice.start" type="date" label="Von" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="invoice.end" type="date" label="Bis" />
      </v-col>
      <template #prepend-actions>
        <InvoicePreviewDialog :src="previewURL">
          <template #activator="{ on, attrs }">
            <v-btn depressed color="primary" v-bind="attrs" v-on="on">Vorschau anzeigen</v-btn>
          </template>
        </InvoicePreviewDialog>
      </template>
    </Form>
  </LayoutDefault>
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      invoice: {
        customer: Number.parseInt(this.$route.params.id, 10),
        address: null,
        start: DateTime.local().set({ day: 15 }).minus({ months: 1 }).toFormat('yyyy-MM-dd'),
        end: DateTime.local().set({ day: 15 }).toFormat('yyyy-MM-dd'),
      },
      addressesChoices: [],
      errors: {},
    }
  },
  head() {
    return {
      title: 'Neue Rechung',
    }
  },
  computed: {
    addresses: {
      get() {
        return this.addressesChoices
      },
      set(addresses) {
        this.addressesChoices = addresses
        this.invoice.address = addresses.find((a) => a.is_primary).id
      },
    },
    previewURL() {
      const searchParams = new URLSearchParams({
        customer: this.invoice.customer,
        start: this.invoice.start,
        end: this.invoice.end,
        address: this.invoice.address,
        token: this.$auth.$storage.getUniversal('_token.local'),
      })
      return `${location.origin}/api/invoicepreview/?${searchParams.toString()}`
    },
  },
  methods: {
    save() {
      return this.$axios.post('/invoices/', this.invoice)
    },
    cancel() {
      if (this.invoice.customer) {
        this.$router.push(`/customers/${this.invoice.customer}#rechnungen`)
      } else {
        this.$router.push('/invoices')
      }
    },
    success() {
      this.notifySuccess('Rechnung erstellt')
      this.$router.push(`/customers/${this.invoice.customer}#rechnungen`)
    },
  },
}
</script>
