<template>
  <v-radio-group v-model="primaryAddress">
    <div v-for="(address, index) in addresses" :key="`address-${address.id}`" class="d-flex flex-column">
      <div class="d-flex align-center">
        <v-btn :disabled="!canDeleteAddress" icon @click="deleteAddress(address)">
          <v-icon color="error">{{ mdiDelete }}</v-icon>
        </v-btn>
        <v-divider vertical class="mx-2" />
        <v-row>
          <v-col cols="12">
            <FieldsText
              v-model="address.address"
              :error-messages="errorsForAddressIndex(index).address"
              label="Adresse"
            />
          </v-col>
          <v-col cols="4">
            <FieldsText
              v-model="address.zip_code"
              :error-messages="errorsForAddressIndex(index).zip_code"
              label="PLZ"
            />
          </v-col>
          <v-col cols="8">
            <FieldsText v-model="address.place" :error-messages="errorsForAddressIndex(index).place" label="Ort" />
          </v-col>
          <v-col cols="12">
            <FieldsCurrency
              v-model.number="address.route_flat"
              :error-messages="errorsForAddressIndex(index).route_flat"
              label="Wegpauschale"
            />
          </v-col>
          <v-col cols="12">
            <v-radio label="Primäradresse" cols="12" :value="address.id" />
          </v-col>
        </v-row>
      </div>
      <v-divider class="my-4" />
    </div>
    <div>
      <v-btn depressed color="primary" @click="newAddress">Weitere Adresse hinzufügen</v-btn>
    </div>
  </v-radio-group>
</template>

<script>
import { mdiDelete } from '@mdi/js'
import cloneDeep from 'lodash/cloneDeep'
import first from 'lodash/first'
import last from 'lodash/last'

export default {
  name: 'EditAddress',
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    errors: {
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
        const primaryAddress = this.addresses.find((address) => address.is_primary === true)
        if (primaryAddress) {
          return primaryAddress
        }
        if (this.addresses.length) {
          return first(this.addresses).id
        }
        return null
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
    canDeleteAddress() {
      return this.addresses.length > 1
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
      this.addresses.push({ id: this.createNewAddressId() })
    },
    deleteAddress(address) {
      this.addresses.splice(this.addresses.indexOf(address), 1)
    },
    errorsForAddressIndex(index) {
      return this.errors[index] || {}
    },
    createNewAddressId() {
      const ids = this.addresses.map((address) => address.id).sort()
      const lastId = last(ids)
      return lastId === null ? 0 : lastId + 1
    },
  },
}
</script>
