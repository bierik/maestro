import noop from 'lodash/noop'

const dateFormat = new Intl.DateTimeFormat('de-CH', { month: 'long', year: 'numeric' })

let api = {
  changeView: noop,
  today: noop,
  prev: noop,
  next: noop,
  getDate: () => new Date(),
}

export const state = () => ({
  currentDate: new Date(),
  view: 'timeGridWeek',
})

export const mutations = {
  setApi(_, _api) {
    api = _api
  },
  setView(state, view) {
    state.view = view
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
  monthView({ commit }) {
    commit('setView', 'dayGridMonth')
    api.changeView('dayGridMonth')
  },
  weekView({ commit }) {
    commit('setView', 'timeGridWeek')
    api.changeView('timeGridWeek')
  },
  applyMobileView({ state }) {
    if (state.view === 'timeGridWeek') {
      api.changeView('timeGridThreeDay')
    } else {
      api.changeView(state.view)
    }
  },
  applyDesktopView({ state: { view } }) {
    api.changeView(view)
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
