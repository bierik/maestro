<template>
  <v-select filled v-bind="$attrs" class="rounded-0" v-on="$listeners">
    <template v-for="(index, name) in $scopedSlots" #[name]="data">
      <slot :name="name" v-bind="data"></slot>
    </template>
  </v-select>
</template>

<script>
export default {
  name: 'AutocompleteField',
  inheritAttrs: false,
}
</script>
