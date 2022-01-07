import isEmpty from 'lodash/isEmpty'
import DateTime from 'luxon/src/datetime'
import Vue from 'vue'

Vue.mixin({
  data() {
    return {
      validators: {
        required(name) {
          return (value) => !isEmpty(value) || `${name} muss ausgefüllt sein`
        },
        datetime(string) {
          const datetime = DateTime.fromFormat(string, 'dd.MM.yyyy, HH:mm')
          return datetime.isValid || `${string} ist kein gültiges Datums-Zeit-Format`
        },
      },
    }
  },
})
