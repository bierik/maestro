export const SEVERITIES = {
  SUCCESS: 'SUCCESS',
  INFO: 'INFO',
  WARNING: 'WARNING',
  ERROR: 'ERROR',
}

export const SEVERITY_COLOR_MAPPING = {
  SUCCESS: 'success',
  INFO: 'info',
  WARNING: 'warning',
  ERROR: 'error',
}

export const state = () => ({
  message: null,
  severity: null,
  show: false,
})

export const mutations = {
  success(state, message) {
    state.message = message
    state.severity = SEVERITIES.SUCCESS
    state.show = true
  },
  info(state, message) {
    state.message = message
    state.severity = SEVERITIES.INFO
    state.show = true
  },
  warning(state, message) {
    state.message = message
    state.severity = SEVERITIES.WARNING
    state.show = true
  },
  error(state, message) {
    state.message = message
    state.severity = SEVERITIES.ERROR
    state.show = true
  },
  close(state) {
    state.show = false
    state.severity = null
    state.message = null
  },
}

export default {
  state,
  mutations,
  namespaced: true,
}
