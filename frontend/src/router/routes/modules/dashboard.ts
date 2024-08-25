import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const DASHBOARD: AppRouteRecordRaw = {
  path: '/dashboard',
  name: 'dashboard',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.dashboard',
    requiresAuth: true,
    icon: 'icon-dashboard',
    order: 0,
    hideInMenu: false,
  },
  children: [
    {
      path: 'workplace',
      name: 'Workplace',
      component: () => import('@/views/dashboard/workplace/index.vue'),
      meta: {
        locale: 'menu.dashboard.workplace',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-desktop',
      },
    },
    {
      path: 'upload',
      name: 'DataUpload',
      component: () => import('@/views/data/upload/index.vue'),
      meta: {
        locale: 'menu.upload',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-upload',
      },
    },
  ],
};

export default DASHBOARD;
