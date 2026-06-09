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
          class="admin-layout__nav-link"
          to="/"
          @click="layoutStore.closeMobileSidebar"
        >
          <i class="pi pi-chart-bar admin-layout__nav-icon" aria-hidden="true" />
          <span class="admin-layout__nav-label">Dashboard Smoke</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="admin-layout__surface">
      <header class="admin-layout__topbar">
        <div class="admin-layout__topbar-start">
          <Button
            :aria-label="layoutStore.sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
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
        </div>
      </header>

      <section class="admin-layout__page-header">
        <p class="admin-layout__eyebrow">{{ sectionLabel }}</p>
        <h2 class="admin-layout__page-title">{{ title }}</h2>
      </section>

      <main class="admin-layout__content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue'
import Button from 'primevue/button'
import { RouterLink } from 'vue-router'

import ThemeModeSwitch from '@/components/shared/ThemeModeSwitch.vue'
import { useLayoutStore } from '@/stores/layout.store'

withDefaults(defineProps<{
  title: string
  sectionLabel?: string
}>(), {
  sectionLabel: 'Phase 1 Scaffold',
})

const layoutStore = useLayoutStore()

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
