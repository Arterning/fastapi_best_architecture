import { createPinia } from 'pinia';
import useAppStore from './modules/app';
import useUserStore from './modules/user';
import useTabBarStore from './modules/tab-bar';
import useDocStore from './modules/doc';

const pinia = createPinia();

export { useAppStore, useUserStore, useTabBarStore, useDocStore };
export default pinia;
