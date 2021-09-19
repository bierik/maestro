<template>
  <LayoutDefault>
    <CustomerForm :customer="customer" />
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
}
</script>

<style></style>
