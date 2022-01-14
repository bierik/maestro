<template>
  <LayoutDefault title="Kunden" narrow>
    <FieldsText v-model="customerFilter.text" hide-details class="shrink" label="Suchen" append-icon="mdi-magnify" />
    <ServerSideIterator :fetch="fetchCustomers" :filter="customerFilter">
      <template #default="{ items }">
        <ListDivided :items="items">
          <template #item="{ item: customer }">
            <v-list-item
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
          </template>
        </ListDivided>
      </template>
    </ServerSideIterator>
    <AddButton to="/customers/new" />
  </LayoutDefault>
</template>

<script>
import { mdiAccount } from '@mdi/js'

export default {
  name: 'CustomersPage',
  data() {
    return { mdiAccount, customerFilter: { text: this.$route.query.text } }
  },
  head() {
    return {
      title: 'Kunden',
    }
  },
  methods: {
    fetchCustomers({ page, itemsPerPage, filter }) {
      const params = {
        page_size: itemsPerPage,
        page,
        ...filter,
      }
      return this.$axios.$get('customers/', { params })
    },
  },
}
</script>
