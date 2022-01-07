<template>
  <v-text-field filled v-bind="$attrs" v-on="$listeners" />
</template>

<script>
export default {
  name: 'TextField',
  inheritAttrs: false,
}
</script>
