import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: {
      title: 'Dashboard',
      requiresAuth: true,
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Others/UserProfile.vue'),
    meta: {
      title: 'Profile',
      requiresAuth: true,
    },
  },
  {
    path: '/organisation',
    name: 'Organisation',
    component: () => import('../views/Pages/OrganisationPage.vue'),
    meta: {
      title: 'Organisation',
      requiresAuth: true,
    },
  },
  {
    path: '/form-elements',
    name: 'Form Elements',
    component: () => import('../views/Forms/FormElements.vue'),
    meta: {
      title: 'Form Elements',
      requiresAuth: true,
    },
  },
  {
    path: '/basic-tables',
    name: 'Basic Tables',
    component: () => import('../views/Tables/BasicTables.vue'),
    meta: {
      title: 'Basic Tables',
      requiresAuth: true,
    },
  },
  {
    path: '/line-chart',
    name: 'Line Chart',
    component: () => import('../views/Chart/LineChart/LineChart.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/bar-chart',
    name: 'Bar Chart',
    component: () => import('../views/Chart/BarChart/BarChart.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/UiElements/Alerts.vue'),
    meta: {
      title: 'Alerts',
      requiresAuth: true,
    },
  },
  {
    path: '/avatars',
    name: 'Avatars',
    component: () => import('../views/UiElements/Avatars.vue'),
    meta: {
      title: 'Avatars',
      requiresAuth: true,
    },
  },
  {
    path: '/badge',
    name: 'Badge',
    component: () => import('../views/UiElements/Badges.vue'),
    meta: {
      title: 'Badge',
      requiresAuth: true,
    },
  },
  {
    path: '/buttons',
    name: 'Buttons',
    component: () => import('../views/UiElements/Buttons.vue'),
    meta: {
      title: 'Buttons',
      requiresAuth: true,
    },
  },
  {
    path: '/images',
    name: 'Images',
    component: () => import('../views/UiElements/Images.vue'),
    meta: {
      title: 'Images',
      requiresAuth: true,
    },
  },
  {
    path: '/videos',
    name: 'Videos',
    component: () => import('../views/UiElements/Videos.vue'),
    meta: {
      title: 'Videos',
      requiresAuth: true,
    },
  },
  {
    path: '/blank',
    name: 'Blank',
    component: () => import('../views/Pages/BlankPage.vue'),
    meta: {
      title: 'Blank',
      requiresAuth: true,
    },
  },
  {
    path: '/error-404',
    name: '404 Error',
    component: () => import('../views/Errors/FourZeroFour.vue'),
    meta: {
      title: '404 Error',
      requiresAuth: true,
    },
  },
  {
    path: '/',
    name: 'Signin',
    component: () => import('../views/Auth/Signin.vue'),
    meta: {
      title: 'Signin',
      requiresAuth: false,
    },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/Auth/Signup.vue'),
    meta: {
      title: 'Signup',
      requiresAuth: false,
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  document.title = `Vue.js ${String(to.meta.title)} | TailAdmin - Vue.js Tailwind CSS Dashboard Template`
  const token = localStorage.getItem('accessToken')
  if (to.meta.requiresAuth && !token) {
    console.warn('No token found. Redirecting to Signin.')
    return next({ name: 'Signin' })
  }
  next()
})

export default router
