import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import * as echarts from 'echarts'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

Vue.config.productionTip = false

//axios.defaults.baseURL = 'http://localhost:5000'
Vue.prototype.$axios = axios
Vue.prototype.$echarts = echarts

Vue.use(Toast, { timeout: 2500 })

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
