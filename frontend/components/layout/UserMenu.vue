<template>
  <v-menu v-if="$vuetify.breakpoint.smAndUp" offset-y>
    <template #activator="{ on, attrs }">
      <v-avatar class="user-menu-avatar" v-bind="attrs" :class="targetClass" v-on="on">
        <v-icon size="24">{{ mdiAccount }}</v-icon>
      </v-avatar>
    </template>
    <v-card>
      <v-card-title>
        {{ $auth.user.full_name }}
      </v-card-title>
      <v-divider />
      <v-card-actions class="pa-0">
        <v-list>
          <v-list-item @click="$auth.logout()">
            <v-list-item-icon>
              <v-icon>{{ mdiLogoutVariant }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title> Logout </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-actions>
    </v-card>
  </v-menu>
  <v-bottom-sheet v-else>
    <template #activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on">
        <v-icon>{{ mdiAccount }}</v-icon>
      </v-btn>
    </template>
    <v-card tile>
      <v-card-title>
        {{ $auth.user.full_name }}
      </v-card-title>
      <v-divider />
      <v-card-actions class="pa-0">
        <v-list>
          <v-list-item @click="$auth.logout()">
            <v-list-item-icon>
              <v-icon>{{ mdiLogoutVariant }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title> Logout </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-actions>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
import { mdiAccount, mdiLogoutVariant } from '@mdi/js'

export default {
  props: {
    targetClass: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      mdiAccount,
      mdiLogoutVariant,
    }
  },
}
</script>
<style>
.user-menu-avatar {
  border: 1px solid white;
}
</style>
