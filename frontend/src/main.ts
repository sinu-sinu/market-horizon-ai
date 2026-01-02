import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Styles
import './assets/styles/main.css'

// Create app
const app = createApp(App)

// Install plugins
app.use(createPinia())
app.use(router)

// Mount
app.mount('#app')
