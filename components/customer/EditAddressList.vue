<template>
  <v-radio-group v-model="primaryAddress">
    <div v-for="address in addresses" :key="`address-${address.id}`" class="d-flex flex-column">
      <div class="d-flex align-center">
        <v-btn icon @click="deleteAddress(address)">
          <v-icon color="error">{{ mdiDelete }}</v-icon>
        </v-btn>
        <v-divider vertical class="mx-2" />
        <div class="grow">
          <v-text-field v-model="address.address" label="Adresse" />
          <v-text-field v-model="address.zip_code" label="PLZ" />
          <v-text-field v-model="address.place" label="Ort" />
          <v-text-field v-model="address.route_flat" label="Wegpauschale" type="number" />
          <v-radio label="Primäradresse" cols="12" :value="address.id" />
        </div>
      </div>
      <v-divider class="my-4" />
    </div>
    <v-btn depressed x-large color="primary" @click="newAddress">Neue Adresse</v-btn>
  </v-radio-group>
</template>

<script>
import cloneDeep from 'lodash/cloneDeep'
import { mdiDelete } from '@mdi/js'
import isEmpty from 'lodash/isEmpty'

export default {
  name: 'EditAddress',
  props: {
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      addresses: cloneDeep(this.value),
      mdiDelete,
    }
  },
  computed: {
    primaryAddress: {
      get() {
        if (isEmpty(this.addresses)) {
          return null
        }
        return this.addresses.find((address) => address.is_primary === true).id
      },
      set(addressId) {
        this.addresses = this.addresses.map((address) => {
          if (address.id === addressId) {
            return Object.assign(address, { is_primary: true })
          }
          return Object.assign(address, { is_primary: false })
        })
      },
    },
  },
  watch: {
    addresses: {
      handler() {
        this.$emit('input', this.addresses)
      },
      deep: true,
    },
  },
  methods: {
    newAddress() {
      if (this.addresses.find((address) => address.is_primary === true)) {
        this.addresses.push({})
      } else {
        this.addresses.push({ is_primary: true, id: 0 })
      }
    },
    deleteAddress(address) {
      this.addresses.splice(this.addresses.indexOf(address), 1)
    },
  },
}
</script>
