<template>
  <v-row class="fill-height align-center justify-center">
    <v-col cols="12" sm="4">
      <v-form class="login-form" @submit.prevent="login">
        <div class="d-flex align-center justify-center mb-6">
          <v-icon left x-large>{{ mdiChartArc }}</v-icon>
          <span class="text-h4"> Maestro </span>
        </div>
        <v-card tile color="primary" class="elevation-0">
          <v-card-title class="white--text"> Login </v-card-title>
          <v-divider />
          <v-card-text>
            <v-text-field
              v-model="credentials.username"
              flat
              class="rounded-0"
              solo
              :error-messages="errors.username"
              label="Benutzername"
              autofocus
            />
            <v-text-field
              v-model="credentials.password"
              type="password"
              solo
              :error-messages="errors.password"
              label="Passwort"
              flat
              class="rounded-0"
            />
          </v-card-text>
          <v-divider />
          <v-card-actions class="py-4">
            <v-btn depressed block tile type="submit">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-col>
  </v-row>
</template>

<script>
import get from 'lodash/get'
import { mdiChartArc } from '@mdi/js'

export default {
  layout: 'blank',
  data() {
    return {
      credentials: {},
      errors: {},
      mdiChartArc,
    }
  },
  head() {
    return {
      title: 'Login',
    }
  },
  methods: {
    async login() {
      try {
        await this.$auth.loginWith('local', { data: this.credentials })
      } catch (error) {
        const errors = get(error, 'response.data', {})
        this.errors = errors
        const nonFieldsErrors = get(errors, 'non_field_errors')
        if (nonFieldsErrors) {
          this.notifyWarning(nonFieldsErrors.join(''))
          this.credentials.password = ''
        }
      }
    },
  },
}
</script>
<style>
.login-form .v-input__slot {
  background-color: #edf3de !important;
}
</style>
