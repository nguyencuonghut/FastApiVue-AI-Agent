<template>
  <div
    :class="[
      'admin-layout',
      {
        'admin-layout--sidebar-collapsed': layoutStore.sidebarCollapsed,
        'admin-layout--mobile-sidebar-open': layoutStore.mobileSidebarOpen,
      },
    ]"
  >
    <button
      v-if="layoutStore.mobileSidebarOpen"
      aria-label="Close menu"
      class="admin-layout__backdrop"
      type="button"
      @click="layoutStore.closeMobileSidebar"
    />

    <aside class="admin-layout__sidebar">
      <div class="admin-layout__sidebar-header">
        <div class="admin-layout__brand">
          <div class="admin-layout__brand-logo" aria-hidden="true">
            <img
              alt=""
              class="admin-layout__brand-logo-image"
              src="/favicon.svg"
            />
          </div>

          <div class="admin-layout__brand-copy">
            <h1 class="admin-layout__brand-title">FastApiVue</h1>
          </div>
        </div>
      </div>

      <nav class="admin-layout__nav">
        <RouterLink
          v-if="permissionStore.can('dashboard.read')"
          class="admin-layout__nav-link"
          to="/"
          @click="layoutStore.closeMobileSidebar"
        >
          <i
            class="pi pi-chart-bar admin-layout__nav-icon"
            aria-hidden="true"
          />
          <span class="admin-layout__nav-label">Dashboard Smoke</span>
        </RouterLink>

        <RouterLink
          v-if="permissionStore.can('users.read')"
          class="admin-layout__nav-link"
          to="/users"
          @click="layoutStore.closeMobileSidebar"
        >
          <i class="pi pi-users admin-layout__nav-icon" aria-hidden="true" />
          <span class="admin-layout__nav-label">Quản lý tài khoản</span>
        </RouterLink>

        <RouterLink
          v-if="permissionStore.can('roles.read')"
          class="admin-layout__nav-link"
          to="/roles"
          @click="layoutStore.closeMobileSidebar"
        >
          <i class="pi pi-key admin-layout__nav-icon" aria-hidden="true" />
          <span class="admin-layout__nav-label">Quản lý vai trò</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="admin-layout__surface">
      <header class="admin-layout__topbar">
        <div class="admin-layout__topbar-start">
          <Button
            :aria-label="
              layoutStore.sidebarCollapsed
                ? 'Expand sidebar'
                : 'Collapse sidebar'
            "
            class="admin-layout__sidebar-toggle"
            icon="pi pi-bars"
            rounded
            severity="secondary"
            text
            @click="layoutStore.toggleSidebar"
          />
        </div>

        <div class="admin-layout__toolbar">
          <div v-if="authStore.currentUser" class="admin-layout__user-chip">
            <span class="admin-layout__user-label">Signed in as</span>
            <strong class="admin-layout__user-value">
              {{ authStore.currentUser.email }}
            </strong>
          </div>
          <ThemeModeSwitch />
          <Button
            class="admin-layout__logout-button"
            icon="pi pi-sign-out"
            label="Logout"
            severity="secondary"
            text
            @click="handleLogout"
          />
        </div>
      </header>

      <section class="admin-layout__page-header">
        <p class="admin-layout__eyebrow">{{ sectionLabel }}</p>
        <h2 class="admin-layout__page-title">{{ title }}</h2>
      </section>

      <main class="admin-layout__content">
        <slot />
      </main>

      <footer class="admin-layout__footer">
        <p class="admin-layout__footer-copy">
          © {{ currentYear }} FastApiVueBoilerplate. Sakai-inspired admin shell.
        </p>
        <p class="admin-layout__footer-meta">
          Timezone mặc định: {{ appTimezone }}
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue'
import Button from 'primevue/button'
import { RouterLink, useRouter } from 'vue-router'

import ThemeModeSwitch from '@/components/shared/ThemeModeSwitch.vue'
import { useAuthStore } from '@/stores/auth.store'
import { useLayoutStore } from '@/stores/layout.store'
import { usePermissionStore } from '@/stores/permission.store'

withDefaults(
  defineProps<{
    title: string
    sectionLabel?: string
  }>(),
  {
    sectionLabel: 'Phase 1 Scaffold',
  },
)

const layoutStore = useLayoutStore()
const authStore = useAuthStore()
const permissionStore = usePermissionStore()
const router = useRouter()
const appTimezone = import.meta.env.VITE_APP_TIMEZONE ?? 'Asia/Ho_Chi_Minh'
const currentYear = new Intl.DateTimeFormat('en-GB', {
  year: 'numeric',
  timeZone: appTimezone,
}).format(new Date())

async function handleLogout() {
  await authStore.logout()
  await router.replace('/login')
}

function handleViewportChange() {
  layoutStore.syncViewport()
}

onMounted(() => {
  handleViewportChange()
  window.addEventListener('resize', handleViewportChange)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleViewportChange)
})
</script>
