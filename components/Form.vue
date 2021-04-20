<template>
  <v-form v-model="valid" v-bind="$attrs" @keyup.enter.native="_save">
    <v-row>
      <slot />
      <v-col cols="12">
        <portal to="append-actions">
          <v-btn :disabled="!valid" icon @click="_save">
            <v-icon>{{ mdiCheck }}</v-icon>
          </v-btn>
          <v-btn v-if="deleteable" icon @click="_destroy">
            <v-icon>{{ mdiTrashCan }}</v-icon>
          </v-btn>
        </portal>
        <portal to="prepend-actions">
          <v-btn icon @click="cancel">
            <v-icon>{{ mdiChevronLeft }}</v-icon>
          </v-btn>
        </portal>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import noop from 'lodash/noop'
import { mdiCheck, mdiChevronLeft, mdiTrashCan } from '@mdi/js'

export default {
  name: 'Form',
  inheritAttrs: false,
  props: {
    value: {
      type: Boolean,
      default: () => true,
    },
    save: {
      type: Function,
      required: true,
    },
    destroy: {
      type: Function,
      default: () => noop,
    },
    cancel: {
      type: Function,
      default: () => noop,
    },
    deleteable: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return {
      mdiCheck,
      mdiChevronLeft,
      mdiTrashCan,
    }
  },
  computed: {
    valid: {
      get() {
        return this.value
      },
      set(valid) {
        this.$emit('input', valid)
      },
    },
  },
  methods: {
    async _destroy() {
      try {
        const response = await this.destroy()
        this.$emit('successDestroy', response)
      } catch (error) {
        this.$emit('serverError', error)
        this.notifyError('Beim Löschen ist ein unerwarteter Fehler aufgetreten')
      }
    },
    async _save() {
      try {
        const response = await this.save()
        this.$emit('success', response)
      } catch (error) {
        if (error.statusCode >= 400 && error.statusCode < 500) {
          this.$emit('update:errors', error.response.data)
          this.notifyWarning('Überprüfen Sie die Eingabefelder auf Fehler')
          this.$emit('clientError', error)
        } else if (error.statusCode >= 500) {
          this.$emit('serverError', error)
          this.notifyError('Beim Speichern ist ein unerwarteter Fehler aufgetreten')
        }
        this.$emit('error', error)
      }
    },
  },
}
</script>
