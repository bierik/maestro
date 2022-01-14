<template>
  <v-form v-model="valid" v-bind="$attrs" class="form" @submit.prevent="_save">
    <v-row>
      <slot />
      <v-col cols="12" class="d-flex">
        <slot name="prepend-actions" />
        <v-spacer />
        <v-btn color="error" depressed class="mr-2" @click="cancel">
          <span>Abbrechen</span>
        </v-btn>
        <v-btn type="submit" :loading="loading" :disabled="!valid" depressed color="success">
          <span>Speichern</span>
        </v-btn>
        <v-btn v-if="deleteable" :loading="loading" depressed color="error" class="ml-2" @click="_destroy">
          <v-icon v-if="$vuetify.breakpoint.smAndDown">{{ mdiTrashCan }}</v-icon>
          <span v-else>Löschen</span>
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import { mdiCheck, mdiChevronLeft, mdiTrashCan } from '@mdi/js'
import get from 'lodash/get'
import noop from 'lodash/noop'

export default {
  name: 'DefaultForm',
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
      loading: false,
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
      this.loading = true
      try {
        const response = await this.destroy()
        this.$emit('successDestroy', response)
      } catch (error) {
        this.$emit('serverError', error)
        this.notifyError('Beim Löschen ist ein unerwarteter Fehler aufgetreten')
      } finally {
        this.loading = false
      }
    },
    async _save() {
      this.loading = true
      try {
        const response = await this.save()
        this.$emit('success', response)
      } catch (error) {
        const statusCode = get(error, 'response.status')
        if (!statusCode) {
          return this.$emit('error', error)
        }
        if (statusCode >= 400 && statusCode < 500) {
          this.$emit('update:errors', error.response.data)
          this.notifyWarning('Überprüfen Sie die Eingabefelder auf Fehler')
          return this.$emit('clientError', error)
        }
        if (statusCode >= 500) {
          this.notifyError('Beim Speichern ist ein unerwarteter Fehler aufgetreten')
          return this.$emit('serverError', error)
        }
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
<style>
.form {
  max-width: 800px;
}
</style>
