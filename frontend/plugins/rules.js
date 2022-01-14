import isEmpty from 'lodash/isEmpty'
import isNull from 'lodash/isNull'
import isUndefined from 'lodash/isUndefined'
import DateTime from 'luxon/src/datetime'
import Vue from 'vue'

Vue.mixin({
  data() {
    return {
      validators: {
        required(name) {
          return (value) => {
            return !isEmpty(value) || !isUndefined(value) || isNull(value) || `${name} muss ausgefüllt sein`
          }
        },
        datetime(string) {
          const datetime = DateTime.fromFormat(string, 'dd.MM.yyyy, HH:mm')
          return datetime.isValid || `${string} ist kein gültiges Datums-Zeit-Format`
        },
        afterToday(dateString) {
          const datetime = DateTime.fromISO(dateString)
          if (!datetime.isValid) {
            return false
          }
          return datetime > DateTime.now().startOf('day').toUTC() || 'Muss nach Heute sein'
        },
      },
    }
  },
})
