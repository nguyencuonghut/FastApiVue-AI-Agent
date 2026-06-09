import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import { configurePrimeVue } from './plugins/primevue'
import { router } from './router'
import { useThemeStore } from './stores/theme.store'
import './styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
configurePrimeVue(app)

const themeStore = useThemeStore(pinia)
themeStore.initialize()

app.mount('#app')
