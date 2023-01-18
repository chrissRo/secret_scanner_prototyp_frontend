
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
import {axiosClient} from "@/api/axiosClient";


const vuetify = createVuetify({
  components,
  directives,
})

const pinia = createPinia();
const app = createApp(App)
registerPlugins(app)

app.use(vuetify)
app.use(router)
app.use(pinia)
app.mount('#app')

app.config.globalProperties.$axios = {...axiosClient}


