import type { App } from 'vue'

import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'

const FastApiVuePreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '#ecf8f6',
      100: '#d1efe9',
      200: '#a8ddd3',
      300: '#74c6b7',
      400: '#46a891',
      500: '#2b8a75',
      600: '#216f5f',
      700: '#1d594d',
      800: '#1a473e',
      900: '#173a34',
      950: '#0b201c',
    },
  },
})

export function configurePrimeVue(app: App<Element>) {
  app.use(PrimeVue, {
    ripple: true,
    theme: {
      preset: FastApiVuePreset,
      options: {
        darkModeSelector: '.app-dark',
      },
    },
  })
  app.use(ToastService)
}
