<template>
  <div
    :class="[
      'admin-layout',
      { 'admin-layout--sidebar-collapsed': layoutStore.sidebarCollapsed },
    ]"
  >
    <aside class="admin-layout__sidebar">
      <div class="admin-layout__brand">
        <span class="admin-layout__brand-mark">FV</span>
        <div>
          <p class="admin-layout__eyebrow">Enterprise Boilerplate</p>
          <h1 class="admin-layout__brand-title">FastApiVue</h1>
        </div>
      </div>

      <nav class="admin-layout__nav">
        <RouterLink class="admin-layout__nav-link" to="/">
          Dashboard Smoke
        </RouterLink>
      </nav>
    </aside>

    <div class="admin-layout__surface">
      <header class="admin-layout__topbar">
        <div>
          <p class="admin-layout__eyebrow">Phase 1 Scaffold</p>
          <h2 class="admin-layout__page-title">{{ title }}</h2>
        </div>

        <div class="admin-layout__toolbar">
          <Button
            class="admin-layout__toggle-button"
            icon="pi pi-bars"
            label="Menu"
            severity="secondary"
            variant="outlined"
            @click="layoutStore.toggleSidebar"
          />
          <ThemeModeSwitch />
        </div>
      </header>

      <main class="admin-layout__content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import { RouterLink } from 'vue-router'

import ThemeModeSwitch from '@/components/shared/ThemeModeSwitch.vue'
import { useLayoutStore } from '@/stores/layout.store'

defineProps<{
  title: string
}>()

const layoutStore = useLayoutStore()
</script>
