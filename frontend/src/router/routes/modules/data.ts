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
        icon: 'icon-file',
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
      path: 'doc-edit',
      name: 'DataDocEdit',
      component: () => import('@/views/data/doc-edit/index.vue'),
      meta: {
        locale: 'menu.doc-edit',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
      },
    },
    {
      path: 'org',
      name: 'DataOrg',
      component: () => import('@/views/data/org/index.vue'),
      meta: {
        locale: 'menu.org',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-stamp',
      },
    },
    {
      path: 'org-detail',
      name: 'DataOrgDetail',
      component: () => import('@/views/data/org-detail/index.vue'),
      meta: {
        locale: 'menu.org-detail',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
      },
    },
    {
      path: 'person',
      name: 'DataPerson',
      component: () => import('@/views/data/person/index.vue'),
      meta: {
        locale: 'menu.person',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-user-group',
      },
    },
    {
      path: 'person-detail',
      name: 'DataPersonDetail',
      component: () => import('@/views/data/person-detail/index.vue'),
      meta: {
        locale: 'menu.person-detail',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
      },
    },
    {
      path: 'subject',
      name: 'DataSubject',
      component: () => import('@/views/data/subject/index.vue'),
      meta: {
        locale: 'menu.subject',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: false,
        icon: 'icon-email',
      },
    },
    {
      path: 'subject-detail',
      name: 'DataSubjectDetail',
      component: () => import('@/views/data/subject-detail/index.vue'),
      meta: {
        locale: 'menu.subject-detail',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
      },
    },
    {
      path: 'person-edit',
      name: 'DataPersonEdit',
      component: () => import('@/views/data/person-edit/index.vue'),
      meta: {
        locale: 'menu.person-edit',
        requiresAuth: true,
        roles: ['*'],
        hideInMenu: true,
      },
    },
  ],
};

export default DATA;
