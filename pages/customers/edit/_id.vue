<template>
  <LayoutDefault>
    <CustomerForm :customer="customer" />
  </LayoutDefault>
</template>

<script>
export default {
  name: 'NewCustomer',
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const customer = await $http.$get(`customers/${id}/`)
    return { customer }
  },
}
</script>

<style></style>
