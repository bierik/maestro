<template>
  <v-tab-item v-bind="$attrs">
    <ServerSideIterator :fetch="fetchFlats">
      <template #default="{ items }">
        <ListDivided :items="items">
          <template #item="{ item: flat }">
            <v-list-item :key="`flat-${flat.id}`" :to="`/flats/${flat.id}`">
              <v-list-item-content>
                <v-list-item-title>
                  {{ flat.name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ flat.price }}
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  {{ flat.created | dateTimeString }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </ListDivided>
      </template>
    </ServerSideIterator>
  </v-tab-item>
</template>

<script>
import path from 'path'

export default {
  inheritAttrs: false,
  methods: {
    fetchFlats({ page, itemsPerPage }) {
      const searchParams = {
        page_size: itemsPerPage,
        page,
      }
      return this.$http.$get(path.join('customers', this.$route.params.id, 'flats/'), { searchParams })
    },
  },
}
</script>
