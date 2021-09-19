import de from 'vuetify/lib/locale/de'

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
    '~/plugins/report',
    { src: '~/plugins/vuex-persist', ssr: false },
    { src: '~/plugins/swiped-events', ssr: false },
  ],
  components: true,
  buildModules: ['@nuxtjs/vuetify'],
  modules: ['@nuxtjs/axios', '@nuxtjs/auth-next', '@nuxtjs/pwa', 'portal-vue/nuxt'],
  axios: {
    prefix: '/api',
    proxy: true,
  },
  proxy: {
    '/api/': 'http://localhost:8000',
    '/media/': 'http://localhost:8000',
  },
  router: {
    middleware: ['auth', 'running-report'],
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
    useWebmanifestExtension: true,
    lang: 'de',
    meta: {
      nativeUI: true,
      theme_color: '#ffffff',
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
