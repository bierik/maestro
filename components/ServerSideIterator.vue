<template>
  <v-data-iterator
    locale="de-CH"
    :items="items.results"
    :server-items-length="items.count"
    v-bind="$attrs"
    :options.sync="options"
    :loading="loading"
    @update:options="debounceLoadItems"
  >
    <template v-for="(index, name) in $scopedSlots" v-slot:[name]="data">
      <slot :name="name" v-bind="data"></slot>
    </template>
  </v-data-iterator>
</template>

<script>
import debounceAsync from 'debounce-async'

export default {
  inheritAttrs: false,
  props: {
    fetch: {
      type: Function,
      default: () => () => [],
    },
    filter: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      items: { count: 0, results: [] },
      options: {},
      loading: true,
    }
  },
  watch: {
    filter: {
      handler() {
        this.debounceLoadItems()
      },
      deep: true,
    },
  },
  methods: {
    async debounceLoadItems() {
      try {
        await this.loadItems()
      } catch (error) {
        if (error !== 'canceled') {
          throw error
        }
      }
    },
    loadItems: debounceAsync(async function loadItems() {
      this.$router.push({
        query: this.filter,
        hash: this.$route.hash,
      })
      this.loading = true
      try {
        this.items = await this.fetch({ ...this.options, filter: this.filter })
      } catch (error) {
        this.items = { count: 0, results: [] }
        throw error
      } finally {
        this.loading = false
      }
    }, 400),
  },
}
</script>

<style></style>
