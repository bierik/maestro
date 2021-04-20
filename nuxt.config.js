export default {
  ssr: false,
  target: 'static',
  loading: false,
  head: {
    titleTemplate: '%s - maestro',
    title: 'maestro',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Manage customers, tasks and invoices.' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  css: [],
  plugins: ['~/plugins/http', '~/plugins/filters', '~/plugins/config', '~/plugins/notification', '~/plugins/rules'],
  components: true,
  buildModules: ['@nuxtjs/vuetify'],
  generate: {
    dir: 'staticfiles',
  },
  modules: ['@nuxt/http', '@nuxtjs/pwa', 'portal-vue/nuxt'],
  http: {
    prefix: '/api',
    headers: {
      Accept: 'application/json',
      'X-CSRFToken': 'bla',
    },
    proxy: true,
  },
  proxy: {
    '/api/': 'http://localhost:8000',
  },
  router: {
    middleware: ['running-report'],
  },
  vuetify: {
    defaultAssets: {
      icons: false,
    },
    customVariables: ['~/assets/variables.scss'],
    icons: {
      iconfont: 'mdiSvg',
    },
  },
  pwa: {
    useWebmanifestExtension: true,
    lang: 'de',
    meta: {
      nativeUI: true,
      theme_color: '#ffffff',
    },
  },
  build: {},
}
