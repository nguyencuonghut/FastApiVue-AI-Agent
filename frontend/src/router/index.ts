import { createRouter, createWebHistory } from 'vue-router'

import DashboardPage from '@/pages/DashboardPage.vue'
import FilesPage from '@/pages/FilesPage.vue'
import ForbiddenPage from '@/pages/ForbiddenPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import RolesPage from '@/pages/RolesPage.vue'
import UsersPage from '@/pages/UsersPage.vue'
import BackupsPage from '@/pages/BackupsPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    return {
      left: 0,
      top: 0,
    }
  },
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
      path: '/files',
      name: 'files',
      component: FilesPage,
      meta: {
        requiresAuth: true,
        requiredPermission: 'files.read',
      },
    },
    {
      path: '/backups',
      name: 'backups',
      component: BackupsPage,
      meta: {
        requiresAuth: true,
        requiredPermission: 'backups.read',
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfilePage,
      meta: {
        requiresAuth: true,
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
