<template>
  <v-app>
    <LayoutNavigation v-if="$vuetify.breakpoint.smAndUp" />
    <v-main>
      <nuxt />
    </v-main>
    <Notification />
    <v-bottom-navigation
      v-if="$vuetify.breakpoint.smAndDown"
      app
      color="white"
      class="elevation-0 justify-start"
      background-color="primary"
    >
      <ReportRunningButton class="grow" />
      <v-btn to="/" nuxt>
        <v-icon>{{ mdiCalendar }}</v-icon>
      </v-btn>
      <v-btn to="/customers" nuxt>
        <v-icon>{{ mdiAccountGroup }}</v-icon>
      </v-btn>
      <v-btn to="/invoices" nuxt>
        <v-icon>{{ mdiReceipt }}</v-icon>
      </v-btn>
      <LayoutUserMenu />
    </v-bottom-navigation>
  </v-app>
</template>

<script>
import { mdiAccountGroup, mdiCalendar, mdiReceipt, mdiAccount } from '@mdi/js'

export default {
  name: 'DefaultLayout',
  data() {
    return { mdiAccountGroup, mdiCalendar, mdiReceipt, mdiAccount }
  },
}
</script>
