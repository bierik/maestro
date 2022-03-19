<template>
  <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
    <v-col cols="12" class="py-0">
      <h2>Personalien</h2>
    </v-col>
    <v-col cols="12">
      <v-alert v-if="errors.non_field_errors" type="warning">
        {{ errors.non_field_errors.join('\n') }}
      </v-alert>
    </v-col>
    <v-col cols="6">
      <FieldsText
        :value="customer.last_name"
        autofocus
        label="Nachname"
        :error-messages="errors.last_name"
        @input="(lastName) => update('last_name', lastName)"
      />
    </v-col>
    <v-col cols="6">
      <FieldsText
        :value="customer.first_name"
        label="Vorname"
        :error-messages="errors.first_name"
        @input="(firstName) => update('first_name', firstName)"
      />
    </v-col>
    <v-col cols="12">
      <FieldsText
        :value="customer.company"
        label="Firmenname"
        :error-messages="errors.company"
        @input="(company) => update('company', company)"
      />
    </v-col>
    <v-col cols="12">
      <FieldsCurrency
        :value="customer.price_per_hour"
        type="number"
        label="Stundenansatz"
        :error-messages="errors.price_per_hour"
        @input="(pricePerHour) => update('price_per_hour', Number.parseInt(pricePerHour, 10))"
      />
    </v-col>
    <v-col cols="12" class="py-0">
      <h2>Adressen</h2>
    </v-col>
    <v-col cols="12">
      <CustomerEditAddressList
        :value="customer.addresses"
        :errors="errors.addresses"
        @input="(addresses) => update('addresses', addresses)"
      />
    </v-col>
  </Form>
</template>

<script>
export default {
  name: 'CustomerForm',
  model: {
    prop: 'customer',
  },
  props: {
    customer: {
      type: Object,
      default: () => ({
        last_name: '',
        first_name: '',
        price_per_hour: 0,
        addresses: [{ id: 0 }],
      }),
    },
  },
  data() {
    return {
      errors: {},
      isEditMode: this.customer.id,
    }
  },
  methods: {
    save() {
      if (this.isEditMode) {
        return this.$axios.$patch(`customers/${this.customer.id}/`, { ...this.customer })
      }
      return this.$axios.$post('customers/', { ...this.customer })
    },
    cancel() {
      if (this.isEditMode) {
        this.$router.push({ name: 'customers-id', params: { id: this.customer.id } })
      } else {
        this.$router.push('/customers')
      }
    },
    success() {
      this.notifySuccess('Kunde wurde gespeichert')
      this.$router.push('/customers')
    },
    update(key, value) {
      this.$emit('input', { ...this.customer, [key]: value })
    },
  },
}
</script>
