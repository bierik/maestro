<template>
  <LayoutDefault title="Kunden" narrow>
    <ServerSideIterator :fetch="fetchCustomers">
      <template #default="{ items }">
        <v-list>
          <v-list-item
            v-for="customer in items"
            :key="`customer-${customer.id}`"
            nuxt
            :to="{ name: 'customers-id', params: { id: customer.id } }"
          >
            <v-list-item-icon>
              <v-icon>{{ mdiAccount }}</v-icon>
            </v-list-item-icon>
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
      </template>
    </ServerSideIterator>
    <AddButton to="/customers/new" />
  </LayoutDefault>
</template>

<script>
import { mdiAccount } from '@mdi/js'

export default {
  name: 'Customers',
  data() {
    return { mdiAccount }
  },
  methods: {
    fetchCustomers({ page, itemsPerPage }) {
      const searchParams = {
        page_size: itemsPerPage,
        page,
      }
      return this.$http.$get('customers/', { searchParams })
    },
  },
}
</script>
