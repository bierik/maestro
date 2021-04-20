import Vue from 'vue'
import isEmpty from 'lodash/isEmpty'

Vue.mixin({
  data() {
    return {
      validators: {
        required(name) {
          return (value) => !isEmpty(value) || `${name} muss ausgefüllt sein`
        },
      },
    }
  },
})
