<template>
  <FieldsSelect
    v-model="template"
    v-bind="$attrs"
    :items="templates"
    label="Vorlage"
    item-text="name"
    item-value="id"
    return-object
  />
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    value: {
      type: Number,
      default: () => null,
    },
  },
  data() {
    return {
      templates: [],
    }
  },
  computed: {
    template: {
      get() {
        return this.value
      },
      set(template) {
        this.$emit('input', template)
      },
    },
  },
  async mounted() {
    try {
      const { results } = await this.$axios.$get('/flat_templates/')
      this.templates = results
    } catch (error) {
      this.notifyError('Die Pauschalvorlagen konnte nicht geladen werden.')
      this.templates = []
    }
  },
}
</script>
