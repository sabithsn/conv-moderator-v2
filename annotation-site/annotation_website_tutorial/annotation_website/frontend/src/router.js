import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('./components/Login.vue')
    },
    {
      path: '/index',
      name: 'index',
      component: () => import('./components/Index.vue')
    },
    {
      path: '/caption',
      name: 'caption',
      component: () => import('./components/Caption.vue')
    },
    {
      path: '/select',
      name: 'select',
      component: () => import('./components/Select.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('./components/Admin.vue')
    }
  ]
})
