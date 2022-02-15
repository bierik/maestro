import noop from 'lodash/noop'

const dateFormat = new Intl.DateTimeFormat('de-CH', { month: 'short', year: 'numeric' })

let api = {
  changeView: noop,
  today: noop,
  prev: noop,
  next: noop,
  getDate: () => new Date(),
}

export const state = () => ({
  currentDate: new Date(),
})

export const mutations = {
  setApi(_, _api) {
    api = _api
  },
  updateCurrentDate(state) {
    state.currentDate = api.getDate()
  },
}

export const actions = {
  prev({ commit }) {
    api.prev()
    commit('updateCurrentDate')
  },
  next({ commit }) {
    api.next()
    commit('updateCurrentDate')
  },
  today({ commit }) {
    api.today()
    commit('updateCurrentDate')
  },
  setView(_, { calendarView, calendarViewDate }) {
    api.changeView(calendarView, calendarViewDate)
  },
  refetchEvents() {
    api.refetchEvents()
  },
}

export const getters = {
  currentDateString(state) {
    return dateFormat.format(state.currentDate)
  },
}

export default {
  state,
  mutations,
  actions,
  getters,
}
