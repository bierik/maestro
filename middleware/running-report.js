export default async function ({ store, route }) {
  if (route.name === 'login') return
  await store.dispatch('report/fetchRunningReport')
}
