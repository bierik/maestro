<template>
  <v-select filled v-bind="$attrs" class="rounded-0" v-on="$listeners" />
</template>

<script>
export default {
  name: 'AutocompleteField',
  inheritAttrs: false,
}
</script>
