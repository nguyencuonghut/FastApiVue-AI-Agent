<template>
  <div class="theme-switch">
    <span class="theme-switch__label">
      {{ themeStore.isDark ? 'Dark mode' : 'Light mode' }}
    </span>
    <ToggleSwitch
      :model-value="themeStore.isDark"
      input-id="theme-mode-toggle"
      @update:model-value="themeStore.toggleMode"
    />
  </div>
</template>

<script setup lang="ts">
import ToggleSwitch from 'primevue/toggleswitch'

import { useThemeStore } from '@/stores/theme.store'

const themeStore = useThemeStore()
</script>
