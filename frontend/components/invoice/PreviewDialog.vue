<template>
  <v-dialog v-model="isOpen" fullscreen :transition="false">
    <v-card class="d-flex flex-column" tile>
      <v-card-title>
        <span class="grow">Rechnungsvorschau</span>
        <v-btn icon @click="isOpen = false"
          ><v-icon>{{ mdiClose }}</v-icon></v-btn
        >
      </v-card-title>
      <v-card-text class="pa-0 grow d-flex flex-column">
        <iframe class="preview-frame grow" :src="previewURL" />
      </v-card-text>
    </v-card>
    <template v-for="(index, name) in $scopedSlots" v-slot:[name]="data">
      <slot :name="name" v-bind="data"></slot>
    </template>
  </v-dialog>
</template>

<script>
import { mdiClose } from '@mdi/js'

export default {
  props: {
    src: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
      mdiClose,
    }
  },
  computed: {
    previewURL() {
      return this.isOpen ? this.src : ''
    },
  },
}
</script>
<style>
.preview-frame {
  border: 0;
}
</style>
