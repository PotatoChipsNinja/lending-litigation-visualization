import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Passwd from '../views/Passwd.vue'
import Search from '../views/Search.vue'
import Label from '../views/Label.vue'
import Court from '../views/Court.vue'
import Decision from '../views/Decision.vue'
import Party from '../views/Party.vue'
import Law from '../views/Law.vue'
import Clause from '../views/Clause.vue'
import Time from '../views/Time.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/',
    component: Home
  },
  {
    path: '/search',
    component: Search
  },
  {
    path: '/label',
    component: Label
  },
  {
    path: '/court',
    component: Court
  },
  {
    path: '/decision',
    component: Decision
  },
  {
    path: '/party',
    component: Party
  },
  {
    path: '/law',
    component: Law
  },
  {
    path: '/time',
    component: Time
  },
  {
    path: '/clause',
    component: Clause
  },
  {
    path: '/passwd',
    component: Passwd
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  let username = localStorage.getItem('username')
  if (!username && to.path != '/login') {
    next('/login')
  } else if (username && to.path == '/login') {
    next('/')
  } else {
    next()
  }
})

router.afterEach(() => {
  document.body.scrollIntoView()
})

export default router
