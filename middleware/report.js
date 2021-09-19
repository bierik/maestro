export default function ({ store }) {
  if (store.state.auth.loggedIn) {
    store.dispatch('report/trackReportDuration')
  }
}
