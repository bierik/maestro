<template>
  <LayoutDefault title="Kunden" narrow>
    <v-list>
      <v-list-item
        v-for="customer in customers"
        :key="`customer-${customer.id}`"
        nuxt
        :to="{ name: 'customers-id', params: { id: customer.id } }"
      >
        <v-list-item-content>
          <v-list-item-title>
            {{ customer.full_name }}
          </v-list-item-title>
          <template v-if="customer.primary_address">
            <v-list-item-subtitle>
              {{ customer.primary_address.address }}
            </v-list-item-subtitle>
            <v-list-item-subtitle>
              {{ customer.primary_address.zip_code }} {{ customer.primary_address.place }}
            </v-list-item-subtitle>
          </template>
          <v-list-item-subtitle v-else> Keine Addresse </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <AddButton to="/customers/new" />
  </LayoutDefault>
</template>

<script>
export default {
  name: 'Customers',
  async asyncData({ $http }) {
    const customers = await $http.$get('customers/')
    return { customers }
  },
}
</script>
