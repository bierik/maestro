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
      class="elevation-0"
      background-color="primary"
    >
      <v-btn to="/" nuxt>
        <!-- <span>Dashboard</span> -->
        <v-icon>{{ mdiViewDashboard }}</v-icon>
      </v-btn>
      <v-btn to="/customers" nuxt>
        <!-- <span>Kunden</span> -->
        <v-icon>{{ mdiAccountGroup }}</v-icon>
      </v-btn>
      <v-btn to="/calendar" nuxt>
        <!-- <span>Kalender</span> -->
        <v-icon>{{ mdiCalendar }}</v-icon>
      </v-btn>
      <v-btn to="/invoices" nuxt>
        <!-- <span>Rechnungen</span> -->
        <v-icon>{{ mdiReceipt }}</v-icon>
      </v-btn>
      <ReportRunningButton />
    </v-bottom-navigation>
  </v-app>
</template>

<script>
import { mdiViewDashboard, mdiAccountGroup, mdiCalendar, mdiReceipt } from '@mdi/js'

export default {
  data() {
    return { mdiViewDashboard, mdiAccountGroup, mdiCalendar, mdiReceipt }
  },
}
</script>
