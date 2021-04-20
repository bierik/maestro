<template>
  <v-container :class="narrow ? 'pa-0' : 'pt-10'" style="height: 100%">
    <v-app-bar app elevation="0">
      <slot name="prepend-actions">
        <portal-target name="prepend-actions" />
      </slot>
      <v-toolbar-title class="ml-2">{{ title }}</v-toolbar-title>
      <v-spacer />
      <slot name="append-actions">
        <portal-target name="append-actions" />
      </slot>
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
