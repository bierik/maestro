<template>
  <v-list v-bind="$attrs">
    <template v-for="(item, index) in items">
      <slot name="item" v-bind="{ item }" />
      <v-divider :key="`divided-list-divider-${index}`" />
    </template>
  </v-list>
</template>

<script>
export default {
  name: 'DividedList',
  props: {
    items: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
