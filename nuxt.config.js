import path from 'path'
import de from 'vuetify/lib/locale/de'

export default {
  rootDir: path.join(__dirname, 'frontend'),
  ssr: false,
  target: 'static',
  loading: false,
  head: {
    titleTemplate: '%s | Maestro',
    title: '…',
  },
  css: ['~/assets/main.css'],
  plugins: [
    '~/plugins/filters',
    '~/plugins/config',
    '~/plugins/notification',
    '~/plugins/rules',
    '~/plugins/full-calendar',
    { src: '~/plugins/vuex-persist', ssr: false },
    { src: '~/plugins/swiped-events', ssr: false },
    { src: '~/plugins/mask', ssr: false },
  ],
  components: true,
  buildModules: ['@nuxtjs/vuetify', '@nuxtjs/pwa'],
  modules: ['@nuxtjs/axios', '@nuxtjs/auth-next', '@nuxtjs/sentry'],
  sentry: {
    disabled: process.env.NODE_ENV !== 'production',
    publishRelease: process.env.NODE_ENV === 'production',
    dsn: process.env.SENTRY_DSN,
    config: {
      release: process.env.SOURCE_COMMIT,
    },
  },
  axios: {
    prefix: '/api',
    proxy: true,
  },
  proxy: {
    '/api/': 'http://localhost:8000',
    '/media/': 'http://localhost:8000',
  },
  router: {
    middleware: ['auth', 'report'],
  },
  vuetify: {
    lang: {
      locales: { de },
      current: 'de',
    },
    defaultAssets: {
      icons: false,
    },
    icons: {
      iconfont: 'mdiSvg',
    },
    theme: {
      options: { customProperties: true },
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
    meta: {
      name: 'Maestro',
      author: 'Bieri Kevin',
      theme_color: '#aac964',
      lang: 'de',
      nativeUI: true,
    },
    manifest: {
      name: 'Maestro',
      short_name: 'Maestro',
      lang: 'de',
      background_color: '#aac964',
    },
  },
  auth: {
    redirect: {
      logout: '/login',
    },
    strategies: {
      local: {
        token: {
          type: 'Token',
        },
        endpoints: {
          login: { url: '/auth/login/', method: 'post' },
          logout: { url: '/auth/logout/', method: 'post' },
          user: { url: '/auth/user/', method: 'get' },
        },
      },
    },
  },
}
