<template>
  <v-autocomplete
    v-model="customer"
    v-bind="$attrs"
    :items="customers"
    label="Kunde"
    item-text="full_name"
    item-value="id"
  />
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    value: {
      type: Number,
      default: () => null,
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
        this.$emit('input', customer)
      },
    },
  },
  async mounted() {
    try {
      this.customers = await this.$http.$get('/customers/')
    } catch (error) {
      this.notifyError('Die Kundenliste konnte nicht geladen werden.')
      this.customers = []
    }
  },
}
</script>
