import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const PERSONAL: AppRouteRecordRaw = {
  path: '/personal',
  name: 'personal',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.personal',
    requiresAuth: true,
    icon: 'icon-desktop',
    order: 2,
    hideInMenu: false,
  },
  children: [
    {
      path: 'star-doc',
      name: 'StarDoc',
      component: () => import('@/views/data/doc-star/index.vue'),
      meta: {
        locale: 'menu.star',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-star',
      },
    },
    {
      path: 'tag',
      name: 'DataTag',
      component: () => import('@/views/data/tag/index.vue'),
      meta: {
        locale: 'menu.tag',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-tag',
      },
    },
  ],
};

export default PERSONAL;
