<template>
  <v-navigation-drawer v-if="$vuetify.breakpoint.smAndUp" permanent app>
    <v-list-item>
      <v-list-item-icon>
        <v-icon>{{ mdiChartArc }}</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="text-h6"> Maestro </v-list-item-title>
        <v-list-item-subtitle> Putztrix </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list class="py-2" dense nav>
      <v-list-item to="/">
        <v-list-item-icon>
          <v-icon>{{ mdiViewDashboard }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item to="/customers">
        <v-list-item-icon>
          <v-icon>{{ mdiAccountGroup }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Kunden</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item to="/calendar">
        <v-list-item-icon>
          <v-icon>{{ mdiCalendar }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Kalender</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item to="/invoices">
        <v-list-item-icon>
          <v-icon>{{ mdiReceipt }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Rechnungen</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <ReportRunningListItem />
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import { mdiViewDashboard, mdiAccountGroup, mdiCalendar, mdiReceipt, mdiChartArc } from '@mdi/js'

export default {
  data() {
    return { mdiViewDashboard, mdiAccountGroup, mdiCalendar, mdiReceipt, mdiChartArc }
  },
}
</script>
