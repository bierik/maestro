import qs from 'qs'

export default function ({ $axios }) {
  $axios.defaults.paramsSerializer = (params) => {
    return qs.stringify(params, { arrayFormat: 'comma' })
  }
}
