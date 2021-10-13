import Vue from 'vue'
import { mapMutations } from 'vuex'

Vue.mixin({
  methods: {
    ...mapMutations({
      notifySuccess: 'notification/success',
      notifyInfo: 'notification/info',
      notifyWarning: 'notification/warning',
      notifyError: 'notification/error',
    }),
  },
})
