import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: () => import('../views/Auth/AuthCallback.vue'),
    meta: {
      title: 'Authenticating...',
      requiresAuth: false,
    },
  },
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
    component: () => import('../views/Pages/UserSettings/UserProfilePage.vue'),
    meta: {
      title: 'Profile',
      requiresAuth: true,
    },
  },
  {
    path: '/company',
    name: 'Company',
    component: () => import('../views/Pages/Administration/CompanyPage.vue'),
    meta: {
      title: 'Company',
      requiresAuth: true,
    },
  },
  {
    path: '/accounts',
    name: 'User Accounts',
    component: () => import('../views/Pages/Administration/AccountAdminPage.vue'),
    meta: {
      title: 'User Accounts',
      requiresAuth: true,
    },
  },
  {
    path: '/user-profile-admin/:id',
    name: 'User Profile Admin',
    component: () => import('../views/Pages/Administration/UserProfileAdminPage.vue'),
    meta: {
      title: 'User Profile Admin',
      requiresAuth: true,
    },
  },
  {
    path: '/client-admin',
    name: 'Client Admin',
    component: () => import('../views/Pages/Client/ClientAdminPage.vue'),
    meta: {
      title: 'Client Admin',
      requiresAuth: true,
    },
  },
  {
    path: '/client/:id',
    name: 'Client Profile',
    component: () => import('../views/Pages/Client/ClientProfileAdminPage.vue'),
    meta: {
      title: 'Client Profile',
      requiresAuth: true,
    },
  },
  {
    path: '/agent-admin',
    name: 'Agent Admin',
    component: () => import('../views/Pages/Agent/AgentAdminPage.vue'),
    meta: {
      title: 'Agent Admin',
      requiresAuth: true,
    },
  },
  {
    path: '/agent/:id',
    name: 'Agent Profile',
    component: () => import('../views/Pages/Agent/AgentProfileAdminPage.vue'),
    meta: {
      title: 'Agent Profile',
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
    path: '/select-tenant',
    name: 'SelectTenant',
    component: () => import('../views/Auth/SelectTenant.vue'),
    meta: {
      title: 'Select Tenant',
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
  routes
})

// Define the expected public hostname and the full public login URL
const publicHostname = 'localhost' 
const publicLoginUrl = 'http://localhost:5173/' // Assuming the signin page is at the root '/'. Adjust if needed.

router.beforeEach((to, from, next) => {
  document.title = `FSP Application - ${String(to.meta.title || 'Welcome')}`

  // Check if navigating to the Signin page and if the hostname is not the public one
  if (to.name === 'Signin' && window.location.hostname !== publicHostname) {
    // Redirect to the public login URL
    window.location.href = publicLoginUrl
    return // Stop the current navigation (use return instead of return false)
  }

  const auth = useAuthStore()

  // If the route requires authentication
  if (to.meta.requiresAuth) {
    // If navigating FROM the callback, assume success and allow passage
    // AuthCallback component handles storing tokens before pushing
    if (from.name === 'AuthCallback') {
      next()
    } 
    // Otherwise, perform the standard authentication check
    else if (!auth.isAuthenticated) {
      next({ name: 'Signin' }) // Redirect to Signin if not authenticated
    } else {
      next() // Proceed if authenticated
    }
  } 
  // If the route does NOT require authentication
  else {
    // Prevent authenticated users from accessing Signin/Signup again? (Optional)
    // if ((to.name === 'Signin' || to.name === 'Signup') && auth.isAuthenticated) {
    //   next({ name: 'Dashboard' }) // Redirect to dashboard
    // } else {
    //   next() // Proceed to public route
    // }
    next() // Allow access to public routes like Signin, AuthCallback, SelectTenant
  }
})

export default router
