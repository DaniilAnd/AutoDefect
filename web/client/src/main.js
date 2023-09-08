import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import YmapPlugin from 'vue-yandex-maps'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

const settings = {
    apiKey: '46b314c8-9465-4e87-89c7-45e8c6cb96b0',
    lang: 'ru_RU',
    coordorder: 'latlong',
    enterprise: false,
    version: '2.1'
  }


const app = createApp(App)

app
    .use(router)
    .use(YmapPlugin, settings)
    .mount('#app')
