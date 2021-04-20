<template>
  <LayoutDefault narrow>
    <template #prepend-actions>
      <v-btn color="transparent" to="/customers" nuxt icon>
        <v-icon color="grey" class="text--darken-2">{{ mdiChevronLeft }}</v-icon>
      </v-btn>
    </template>
    <template #append-actions>
      <v-btn color="transparent" nuxt :to="{ name: 'customers-edit-id', params: { id: customer.id } }" icon>
        <v-icon color="grey" class="text--darken-2">{{ mdiPencil }}</v-icon>
      </v-btn>
    </template>
    <v-tabs v-model="tab" fixed-tabs>
      <v-tab to="#personalien">Personalien</v-tab>
      <v-tab to="#rapporte">Rapporte</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item value="personalien" :transition="false" :reverse-transition="false">
        <v-list>
          <v-subheader> Personalien </v-subheader>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.last_name }}
              </v-list-item-title>
              <v-list-item-subtitle> Nachname </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.first_name }}
              </v-list-item-title>
              <v-list-item-subtitle> Vorname </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ customer.price_per_hour }}
              </v-list-item-title>
              <v-list-item-subtitle> Stundenansatz </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-subheader> Adressen </v-subheader>
          <v-list-item v-for="address in customer.addresses" :key="`address-${address.id}`">
            <v-list-item-icon>
              <v-icon v-if="address.is_primary">{{ mdiRadioboxMarked }}</v-icon>
              <v-icon v-else>{{ mdiRadioboxBlank }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ address.address }}
              </v-list-item-title>
              <v-list-item-subtitle> {{ address.zip_code }} {{ address.place }} </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
      <v-tab-item value="rapporte" :transition="false" :reverse-transition="false">
        <v-list>
          <v-list-item v-for="report in reports" :key="`report-${report.id}`">
            <v-list-item-content>
              <v-list-item-title>
                {{ report.title }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ report.start | dateTimeString }}
              </v-list-item-subtitle>
              <v-list-item-subtitle v-if="report.end">
                {{ report.end | dateTimeString }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action v-if="!report.end">
              <v-btn icon to="/report">
                <v-icon color="primary">{{ mdiAlarm }}</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-tab-item>
    </v-tabs-items>
  </LayoutDefault>
</template>

<script>
import { mdiPencil, mdiChevronLeft, mdiRadioboxMarked, mdiRadioboxBlank, mdiAlarm } from '@mdi/js'

export default {
  name: 'ShowCustomer',
  async asyncData({
    $http,
    route: {
      params: { id },
    },
  }) {
    const customer = await $http.$get(`customers/${id}/`)
    return { customer }
  },
  data() {
    return {
      tab: 'personalien',
      reports: [],
      mdiChevronLeft,
      mdiPencil,
      mdiRadioboxMarked,
      mdiRadioboxBlank,
      mdiAlarm,
    }
  },
  watch: {
    tab: {
      async handler() {
        this.reports = await this.$http.$get(`customers/${this.customer.id}/reports/`)
      },
      immediate: true,
    },
  },
}
</script>
