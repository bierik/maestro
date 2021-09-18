<template>
  <LayoutDefault title="Pauschal">
    <Form :cancel="cancel" :save="save" :errors.sync="errors" @success="success">
      <v-col cols="12">
        <CustomerSelect v-model="flat.customer_id" :error-messages="errors.customer_id" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="flat.name" label="Name" :error-messages="errors.title" />
      </v-col>
      <v-col cols="12">
        <FieldsText v-model="flat.price" type="number" postfix="CHF" label="Preis" :error-messages="errors.price" />
      </v-col>
    </Form>
  </LayoutDefault>
</template>

<script>
export default {
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const flat = await $http.$get(`flats/${id}/`)
    return {
      flat: {
        name: flat.name,
        price: flat.price,
        customer_id: flat.customer.id,
        id: flat.id,
      },
    }
  },
  data() {
    return {
      errors: {},
    }
  },
  methods: {
    save() {
      return this.$http.$patch(`flats/${this.flat.id}/`, this.flat)
    },
    cancel() {
      this.$router.push(`/customers/${this.flat.customer_id}#pauschale`)
    },
    success() {
      this.notifySuccess('Pauschal wurde aktualisiert')
      this.$router.push(`/customers/${this.flat.customer_id}#pauschale`)
    },
  },
}
</script>
