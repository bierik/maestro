export const state = () => ({
  runningReport: null,
})

export const mutations = {
  setRunningReport(state, report) {
    state.runningReport = report
  },
}

export const actions = {
  async fetchRunningReport({ commit }) {
    const report = await this.$http.$get('/reports/running/')
    commit('setRunningReport', report)
  },
}

export const getters = {
  hasRunningReport(state) {
    return !!state.runningReport
  },
}

export default {
  state,
  mutations,
  actions,
  getters,
}
