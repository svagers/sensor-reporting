import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import './style.css'
import App from './App.vue'

const app = createApp(App)
app.use(PrimeVue, { unstyled: false })
app.use(ToastService)
app.mount('#app')
