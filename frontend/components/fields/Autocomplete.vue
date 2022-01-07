<template>
  <v-select filled v-bind="$attrs" v-on="$listeners" />
</template>

<script>
export default {
  name: 'AutocompleteField',
  inheritAttrs: false,
}
</script>
