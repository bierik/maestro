<template>
  <LayoutDefault title="Neuer Kunde erfassen">
    <CustomerForm v-model="customer" />
  </LayoutDefault>
</template>

<script>
export default {
  name: 'NewCustomer',
  data() {
    return {
      customer: undefined,
    }
  },
  head() {
    return {
      title: 'Neuer Kunde',
    }
  },
}
</script>

<style></style>
