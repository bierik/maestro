<template>
  <FieldsSelect
    v-model="customer"
    v-bind="$attrs"
    :items="customers"
    label="Kunde"
    item-text="full_name"
    item-value="id"
    return-object
  />
</template>

<script>
export default {
  name: 'SelectField',
  inheritAttrs: false,
  props: {
    value: {
      type: Number,
      default: () => null,
    },
    addresses: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      customers: [],
    }
  },
  computed: {
    customer: {
      get() {
        return this.value
      },
      set(customer) {
        this.$emit('input', customer.id)
        this.$emit('update:addresses', customer.addresses)
      },
    },
  },
  async mounted() {
    try {
      const { results: customers } = await this.$axios.$get('/customers/')
      this.customers = customers
    } catch (error) {
      this.notifyError('Die Kundenliste konnte nicht geladen werden.')
      this.customers = []
    }
  },
}
</script>
