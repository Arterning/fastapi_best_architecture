import { DEFAULT_LAYOUT } from '../base';
import { AppRouteRecordRaw } from '../types';

const DATA: AppRouteRecordRaw = {
  path: '/data',
  name: 'data',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.data',
    requiresAuth: true,
    icon: 'icon-common',
    order: 1,
    hideInMenu: false,
  },
  children: [
    {
      path: 'doc',
      name: 'DataDoc',
      component: () => import('@/views/data/doc/index.vue'),
      meta: {
        locale: 'menu.doc',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
      },
    },
    {
      path: 'star-doc',
      name: 'StarDoc',
      component: () => import('@/views/data/doc-star/index.vue'),
      meta: {
        locale: 'menu.star',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
      },
    },
    {
      path: 'doc-detail',
      name: 'DataDocDetail',
      component: () => import('@/views/data/doc-detail/index.vue'),
      meta: {
        locale: 'menu.doc-detail',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
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
      },
    },
  ],
};

export default DATA;
