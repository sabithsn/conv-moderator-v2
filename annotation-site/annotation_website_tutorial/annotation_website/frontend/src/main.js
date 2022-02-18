import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Vue from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import VueResource from 'vue-resource'
import locale from 'element-ui/lib/locale/lang/en'


Vue.use(VueResource)
Vue.use(ElementUI, { locale })
Vue.prototype.$axios = axios
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
