import get from 'lodash/get'
import DateTime from 'luxon/src/datetime'

export const state = () => ({
  runningReport: null,
  runningReportDurationInterval: null,
  runningReportDuration: '',
})

export const mutations = {
  setRunningReport(state, report) {
    state.runningReport = report
  },
  setRunningReportDuration(state, duration) {
    state.runningReportDuration = duration
  },
  setRunningReportDurationInterval(state, interval) {
    state.runningReportDurationInterval = interval
  },
}

export const actions = {
  async fetchRunningReport({ commit }) {
    const report = await this.$axios.$get('/reports/running/')
    commit('setRunningReport', report)
  },
  computeRunningReportDuration({ commit, getters: { hasRunningReport }, state: { runningReport } }) {
    if (hasRunningReport) {
      const start = DateTime.fromISO(runningReport.start)
      commit('setRunningReportDuration', DateTime.local().diff(start).toFormat('hh:mm'))
    } else {
      commit('setRunningReportDuration', '')
    }
  },
  async trackReportDuration({ commit, dispatch, state: { runningReportDurationInterval } }) {
    await dispatch('fetchRunningReport')
    dispatch('computeRunningReportDuration')
    clearInterval(runningReportDurationInterval)
    const interval = setInterval(() => {
      dispatch('computeRunningReportDuration')
    }, 60 * 1000)
    commit('setRunningReportDurationInterval', interval)
  },
}

export const getters = {
  hasRunningReport(state) {
    return !!state.runningReport
  },
  runningReportCustomer(state) {
    return get(state.runningReport, 'customer.full_name', '')
  },
}

export default {
  state,
  mutations,
  actions,
  getters,
}
