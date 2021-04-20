import cookie from 'cookie'

export default function ({ $http }) {
  $http.onRequest((config) => {
    const { csrftoken } = cookie.parse(document.cookie)
    config.headers.set('X-CSRFToken', csrftoken)
  })
}
