import { createRouter, createWebHistory } from 'vue-router'

import DashboardPage from '@/pages/DashboardPage.vue'
import ForbiddenPage from '@/pages/ForbiddenPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RolesPage from '@/pages/RolesPage.vue'
import UsersPage from '@/pages/UsersPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: {
        guestOnly: true,
      },
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardPage,
      meta: {
        requiresAuth: true,
        requiredPermission: 'dashboard.read',
      },
    },
    {
      path: '/users',
      name: 'users',
      component: UsersPage,
      meta: {
        requiresAuth: true,
        requiredPermission: 'users.read',
      },
    },
    {
      path: '/roles',
      name: 'roles',
      component: RolesPage,
      meta: {
        requiresAuth: true,
        requiredPermission: 'roles.read',
      },
    },
    {
      path: '/forbidden',
      name: 'forbidden',
      component: ForbiddenPage,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})
