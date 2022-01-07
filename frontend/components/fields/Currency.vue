<template>
  <FieldsText v-bind="$attrs" type="number" suffix="CHF" v-on="$listeners" />
</template>

<script>
export default {
  name: 'CurrencyField',
  inheritAttrs: false,
}
</script>
