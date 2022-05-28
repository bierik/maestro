<template>
  <v-container class="fill-height flex-column align-stretch" :class="narrow ? 'pa-0' : 'pb-16'">
    <v-app-bar app elevation="0" color="primary" dark height="67" class="app-bar pl-2">
      <slot name="prepend-actions" />
      <v-toolbar-title class="ml-2">
        <slot name="title" />
      </v-toolbar-title>
      <v-spacer />
      <slot name="append-actions" />
      <LayoutUserMenu v-if="$vuetify.breakpoint.smAndUp" target-class="ml-4" />
    </v-app-bar>
    <slot />
  </v-container>
</template>

<script>
export default {
  name: 'DefaultLayout',
  props: {
    title: {
      type: String,
      default: () => '',
    },
    narrow: {
      type: Boolean,
      default: () => false,
    },
  },
}
</script>
<style>
.v-app-bar > .v-toolbar__content {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
