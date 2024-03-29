<template>
  <v-data-iterator
    locale="de-CH"
    :items="items.results"
    :server-items-length="items.count"
    v-bind="$attrs"
    :options.sync="options"
    :loading="loading"
    class="grow d-flex flex-column"
    hide-default-footer
    @update:options="debounceLoadItems"
  >
    <template #header="{ pagination, options: paginationOptions, updateOptions }">
      <div class="d-flex shrink align-center">
        <v-data-footer
          :pagination="pagination"
          :options="paginationOptions"
          :items-per-page-options="[]"
          class="grow"
          @update:options="updateOptions"
        />
        <div class="pr-2">
          <slot name="append-header" />
        </div>
      </div>
      <v-divider />
    </template>
    <template v-for="name in $scopedSlots" #[name]="data">
      <slot :name="name" v-bind="data"></slot>
    </template>
    <template #default="attrs">
      <div class="grow">
        <slot name="default" v-bind="attrs" />
      </div>
    </template>
    <template #no-data>
      <div class="d-flex align-center justify-center flex-column py-8">
        <span class="text-h6 font-weight-light">Keine Einträge gefunden</span>
      </div>
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
      options: { itemsPerPage: 100 },
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

<style>
.v-data-iterator > div {
  flex-grow: 1;
  flex-shrink: 0;
}

.v-data-iterator > .v-data-footer {
  flex-grow: 0;
  flex-shrink: 1;
}

.v-data-footer {
  padding-top: 6px;
  padding-bottom: 6px;
}
</style>
