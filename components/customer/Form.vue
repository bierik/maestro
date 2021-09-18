<template>
  <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
    <v-col cols="12" class="py-0">
      <h2>Personalien</h2>
    </v-col>
    <v-col cols="6">
      <FieldsText v-model="customer.last_name" autofocus label="Nachname" :error-messages="errors.last_name" />
    </v-col>
    <v-col cols="6">
      <FieldsText v-model="customer.first_name" label="Vorname" :error-messages="errors.first_name" />
    </v-col>
    <v-col cols="12">
      <FieldsCurrency
        v-model.number="customer.price_per_hour"
        type="number"
        label="Stundenansatz"
        :error-messages="errors.price_per_hour"
      />
    </v-col>
    <v-col cols="12" class="py-0">
      <h2>Adressen</h2>
    </v-col>
    <v-col cols="12">
      <CustomerEditAddressList v-model="customer.addresses" :errors="errors.addresses" />
    </v-col>
  </Form>
</template>

<script>
export default {
  name: 'CustomerForm',
  props: {
    customer: {
      type: Object,
      default: () => ({}),
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
        return this.$http.$patch(`customers/${this.customer.id}/`, { ...this.customer })
      }
      return this.$http.$post('customers/', { ...this.customer })
    },
    cancel() {
      this.$router.push({ name: 'customers-id', params: { id: this.customer.id } })
    },
    success() {
      this.notifySuccess('Kunde wurde gespeichert')
      this.$router.push('/customers')
    },
  },
}
</script>
