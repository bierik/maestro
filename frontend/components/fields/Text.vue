<template>
  <v-text-field filled v-bind="$attrs" class="rounded-0" autocomplete="please-do-not-autocomplete" v-on="$listeners" />
</template>

<script>
export default {
  name: 'TextField',
  inheritAttrs: false,
}
</script>
