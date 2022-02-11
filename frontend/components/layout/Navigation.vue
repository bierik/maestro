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

    <v-list class="py-2" nav>
      <v-list-item to="/" :exact="false">
        <v-list-item-icon>
          <v-icon>{{ mdiCalendar }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Kalender</v-list-item-title>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn depressed small to="/calendar/new">
            <v-icon>{{ mdiPlus }}</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
      <v-list-item to="/customers" :exact="false">
        <v-list-item-icon>
          <v-icon>{{ mdiAccountGroup }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Kunden</v-list-item-title>
        </v-list-item-content>
        <v-btn depressed small to="/customers/new">
          <v-icon>{{ mdiPlus }}</v-icon>
        </v-btn>
      </v-list-item>
      <v-list-item to="/invoices" :exact="false">
        <v-list-item-icon>
          <v-icon>{{ mdiReceipt }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Rechnungen</v-list-item-title>
        </v-list-item-content>
        <v-btn depressed small to="/invoices/new">
          <v-icon>{{ mdiPlus }}</v-icon>
        </v-btn>
      </v-list-item>
      <ReportRunningListItem />
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import { mdiAccountGroup, mdiCalendar, mdiReceipt, mdiChartArc, mdiPlus } from '@mdi/js'

export default {
  name: 'DefaultNavigation',
  data() {
    return { mdiAccountGroup, mdiCalendar, mdiReceipt, mdiChartArc, mdiPlus }
  },
}
</script>
