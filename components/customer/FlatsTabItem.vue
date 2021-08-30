<template>
  <v-tab-item v-bind="$attrs">
    <ServerSideIterator :fetch="fetchFlats">
      <template #default="{ items }">
        <v-list>
          <v-list-item v-for="flat in items" :key="`flat-${flat.id}`" :to="`/flats/${flat.id}`">
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
        </v-list>
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
