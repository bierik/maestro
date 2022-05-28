<template>
  <LayoutDefault>
    <CustomerForm v-model="customer">
      <template #prepend-actions>
        <v-btn v-if="customer.is_active" depressed color="error" @click="deactivate">Deaktivieren</v-btn>
        <v-btn v-else depressed color="success" @click="activate">Aktivieren</v-btn>
      </template>
    </CustomerForm>
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
  methods: {
    async deactivate() {
      try {
        await this.$axios.$post(`customers/${this.customer.id}/deactivate/`)
        this.notifySuccess('Kunde wurde deaktiviert')
        this.$router.push({ name: 'customers' })
      } catch (error) {
        this.notifyError('Beim Deaktivieren ist ein Fehler aufgetreten.')
        throw error
      }
    },
    async activate() {
      try {
        await this.$axios.$post(`customers/${this.customer.id}/activate/`)
        this.notifySuccess('Kunde wurde aktiviert')
        this.$router.push({ name: 'customers' })
      } catch (error) {
        this.notifyError('Beim Aktivieren ist ein Fehler aufgetreten.')
        throw error
      }
    },
  },
}
</script>

<style></style>
