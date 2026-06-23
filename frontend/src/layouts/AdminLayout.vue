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
            <h1 class="admin-layout__brand-title">{{ appName }}</h1>
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

        <RouterLink
          v-if="permissionStore.can('files.read')"
          class="admin-layout__nav-link"
          to="/files"
          @click="layoutStore.closeMobileSidebar"
        >
          <i class="pi pi-file admin-layout__nav-icon" aria-hidden="true" />
          <span class="admin-layout__nav-label">Quản lý tập tin</span>
        </RouterLink>

        <RouterLink
          v-if="permissionStore.can('backups.read')"
          class="admin-layout__nav-link"
          to="/backups"
          @click="layoutStore.closeMobileSidebar"
        >
          <i class="pi pi-database admin-layout__nav-icon" aria-hidden="true" />
          <span class="admin-layout__nav-label">Quản lý sao lưu</span>
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
          <ThemeModeSwitch />
          <button
            v-if="authStore.currentUser"
            aria-label="Mở menu tài khoản"
            class="admin-layout__profile-trigger"
            type="button"
            @click="toggleProfileMenu"
          >
            <span class="admin-layout__profile-avatar" aria-hidden="true">
              <img
                v-if="authStore.currentUser.avatarUrl"
                :src="authStore.currentUser.avatarUrl"
                alt=""
                class="admin-layout__profile-avatar-image"
              />
              <span v-else class="admin-layout__profile-avatar-fallback">
                {{ profileInitials }}
              </span>
            </span>
            <span class="admin-layout__profile-copy">
              <span class="admin-layout__profile-name">{{ displayUserName }}</span>
            </span>
          </button>
          <Menu
            ref="profileMenuRef"
            :model="profileMenuItems"
            popup
            class="admin-layout__profile-menu"
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
          © {{ currentYear }} {{ appName }}. Tất cả quyền được bảo lưu.
        </p>
        <div class="admin-layout__footer-meta">
          <span :class="['admin-layout__footer-status', { 'admin-layout__footer-status--offline': !isOnline }]">
            <span class="admin-layout__footer-status-dot" aria-hidden="true" />
            {{ isOnline ? 'Hệ thống trực tuyến' : 'Hệ thống ngoại tuyến' }}
          </span>
          <span class="admin-layout__footer-divider" aria-hidden="true">|</span>
          <span class="admin-layout__footer-version">v0.1.0</span>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import Menu from 'primevue/menu'
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
const profileMenuRef = ref<InstanceType<typeof Menu> | null>(null)
const appTimezone = import.meta.env.VITE_APP_TIMEZONE ?? 'Asia/Ho_Chi_Minh'
const appName = import.meta.env.VITE_APP_NAME || 'FastApiVue'
const isOnline = ref(true)
let healthTimer: number | null = null

async function checkSystemHealth() {
  try {
    const response = await window.fetch('/api/v1/health', {
      method: 'GET',
      cache: 'no-store',
    })
    isOnline.value = response.ok
  } catch {
    isOnline.value = false
  }
}
const currentYear = new Intl.DateTimeFormat('en-GB', {
  year: 'numeric',
  timeZone: appTimezone,
}).format(new Date())
const displayUserName = computed(() => {
  const fullName = authStore.currentUser?.fullName?.trim()
  if (fullName) {
    return fullName
  }

  return authStore.currentUser?.email?.trim() ?? 'Người dùng'
})
const profileInitials = computed(() => {
  const fullName = authStore.currentUser?.fullName?.trim()
  if (fullName) {
    const parts = fullName.split(/\s+/).filter(Boolean)
    return parts
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase() ?? '')
      .join('')
  }

  const email = authStore.currentUser?.email?.trim()
  return email ? email.slice(0, 2).toUpperCase() : 'FV'
})
const profileMenuItems = [
  {
    label: 'Hồ sơ',
    icon: 'pi pi-user',
    command: async () => {
      await router.push('/profile')
    },
  },
  {
    label: 'Logout',
    icon: 'pi pi-sign-out',
    command: async () => {
      await handleLogout()
    },
  },
]

async function handleLogout() {
  await authStore.logout()
  await router.replace('/login')
}

function toggleProfileMenu(event: globalThis.MouseEvent) {
  profileMenuRef.value?.toggle(event)
}

function handleViewportChange() {
  layoutStore.syncViewport()
}

onMounted(() => {
  handleViewportChange()
  window.addEventListener('resize', handleViewportChange)
  checkSystemHealth()
  healthTimer = window.setInterval(checkSystemHealth, 15000)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleViewportChange)
  if (healthTimer !== null) {
    window.clearInterval(healthTimer)
  }
})
</script>
