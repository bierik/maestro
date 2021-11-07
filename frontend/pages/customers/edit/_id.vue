<template>
  <LayoutDefault>
    <CustomerForm v-model="customer" />
  </LayoutDefault>
</template>

<script>
export default {
  name: 'NewCustomer',
  async asyncData({
    $axios,
    route: {
      params: { id },
    },
  }) {
    const customer = await $axios.$get(`customers/${id}/`)
    return { customer }
  },
  head() {
    return {
      title: this.customer.full_name,
    }
  },
}
</script>

<style></style>
