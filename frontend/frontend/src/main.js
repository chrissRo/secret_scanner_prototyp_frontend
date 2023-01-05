
// Components
import App from './App.vue'
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import { createApp } from 'vue'
import router from "@/router/index.js";

// Plugins
import { registerPlugins } from '@/plugins'
import {createPinia} from "pinia";
import axios from "axios";


const vuetify = createVuetify({
  components,
  directives,
})

const pinia = createPinia();
const app = createApp(App)

/*
Axios Setup
 */

let axiosBase = axios.create({
  baseURL: 'http://localhost:8000'
})

axiosBase.defaults.headers.common['Access-Control-Allow-Origin'] = 'http://localhost:8000'
app.config.globalProperties.$axios = {...axiosBase}


registerPlugins(app)

app.use(vuetify)
app.use(router)
app.use(pinia)
app.mount('#app')
