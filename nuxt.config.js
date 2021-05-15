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
  css: ['~/assets/main.css'],
  plugins: [
    '~/plugins/http',
    '~/plugins/filters',
    '~/plugins/config',
    '~/plugins/notification',
    '~/plugins/rules',
    '~/plugins/full-calendar',
  ],
  components: true,
  buildModules: ['@nuxtjs/vuetify'],
  modules: ['@nuxt/http', '@nuxtjs/pwa', 'portal-vue/nuxt'],
  http: {
    prefix: '/api',
    proxy: true,
  },
  proxy: {
    '/api/': 'http://localhost:8000',
    '/media/': 'http://localhost:8000',
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
    theme: {
      themes: {
        light: {
          primary: '#aac964',
          created: '#e07a5f',
          sent: '#f2cc8f',
          payed: '#aac964',
          archived: '#9299dd',
        },
      },
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
  build: {
    babel: {
      plugins: [['@babel/plugin-proposal-class-properties', { loose: false }]],
    },
  },
}
