<template>
  <v-tab-item v-bind="$attrs">
    <v-list-item v-for="flat in flats" :key="`flat-${flat.id}`" :to="`/flats/${flat.id}`">
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
  </v-tab-item>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    flats: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
