<template>
  <v-tab-item v-bind="$attrs">
    <v-list>
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
          <v-list-item-subtitle> Wegpauschale: {{ address.route_flat | currency }} </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-tab-item>
</template>

<script>
import { mdiRadioboxMarked, mdiRadioboxBlank } from '@mdi/js'

export default {
  inheritAttrs: false,
  props: {
    customer: {
      type: Object,
      default: () => ({ addresses: [] }),
    },
  },
  data() {
    return {
      mdiRadioboxMarked,
      mdiRadioboxBlank,
    }
  },
}
</script>
