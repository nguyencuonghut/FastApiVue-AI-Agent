<template>
  <section class="login-page">
    <div class="login-page__panel">
      <div class="login-page__hero">
        <div class="login-page__brand">
          <img alt="" class="login-page__brand-logo" src="/favicon.svg" />
          <div>
            <p class="login-page__eyebrow">Phase 2 Auth Foundation</p>
            <h1 class="login-page__title">Đăng nhập quản trị</h1>
          </div>
        </div>

        <p class="login-page__lead">
          Boilerplate này dùng access token ngắn hạn trong memory và refresh
          session qua <code>httpOnly cookie</code>.
        </p>
      </div>

      <Card class="login-page__card">
        <template #title> Sign In </template>
        <template #content>
          <form class="login-page__form" @submit.prevent="submitLogin">
            <div class="login-page__field">
              <label class="login-page__label required" for="email"
                >Email</label
              >
              <InputText
                id="email"
                v-model="email"
                autocomplete="username"
                class="login-page__input"
                fluid
                type="email"
                v-bind="emailProps"
              />
              <small v-if="errors.email" class="login-page__error">
                {{ errors.email }}
              </small>
            </div>

            <div class="login-page__field">
              <label class="login-page__label required" for="password"
                >Mật khẩu</label
              >
              <Password
                id="password"
                v-model="password"
                :feedback="false"
                autocomplete="current-password"
                class="login-page__password"
                fluid
                toggle-mask
                v-bind="passwordProps"
              />
              <small v-if="errors.password" class="login-page__error">
                {{ errors.password }}
              </small>
            </div>

            <Button
              :disabled="isSubmitting"
              :loading="isSubmitting"
              class="login-page__submit"
              label="Đăng nhập"
              type="submit"
            />
          </form>
        </template>
      </Card>
    </div>
  </section>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import { useRouter, useRoute } from 'vue-router'

import { useLoginPage } from '@/composables/useLoginPage'

const route = useRoute()
const router = useRouter()

const {
  email,
  emailProps,
  errors,
  isSubmitting,
  password,
  passwordProps,
  submitLogin,
} = useLoginPage(async () => {
  const redirectTarget =
    typeof route.query.redirect === 'string' ? route.query.redirect : '/'

  await router.replace(redirectTarget)
})
</script>
