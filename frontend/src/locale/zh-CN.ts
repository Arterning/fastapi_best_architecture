import localeLogin from '@/views/login/locale/zh-CN';
import localeSysMenu from '@/views/admin/menu/locale/zh-CN';
import localeWorkplace from '@/views/dashboard/workplace/locale/zh-CN';
import localeLogLogin from '@/views/log/login/locale/zh-CN';
import localeIconPicker from '@/components/icon-picker/locale/zh-CN';
import localeLogOpera from '@/views/log/opera/locale/zh-CN';
import localeSysDept from '@/views/admin/dept/locale/zh-CN';
import localeSysApi from '@/views/admin/api/locale/zh-CN';
import localeServerMonitor from '@/views/monitor/server/locale/zh-CN';
import localeRedisMonitor from '@/views/monitor/redis/locale/zh-CN';
import localeSysUser from '@/views/admin/user/locale/zh-CN';
import localeSysRole from '@/views/admin/role/locale/zh-CN';
import localDoc from '@/views/data/doc/locale/zh-CN';
import localeSettings from './zh-CN/settings';

export default {
  'menu.dashboard': '仪表盘',
  'menu.server.dashboard': '仪表盘-服务端',
  'menu.server.workplace': '工作台-服务端',
  'menu.system': '系统管理',
  'menu.log': '日志',
  'menu.monitor': '系统监控',
  'menu.server.monitor': '实时监控-服务端',
  'menu.list': '列表页',
  'menu.result': '结果页',
  'menu.exception': '异常页',
  'menu.form': '表单页',
  'menu.profile': '详情页',
  'menu.visualization': '数据可视化',
  'menu.user': '个人中心',
  'menu.arcoWebsite': 'Arco Design',
  'menu.faq': '常见问题',
  'navbar.docs': '文档中心',
  'navbar.action.locale': '切换为中文',
  'modal.title.tips': '温馨提示',
  'modal.title.tips.delete': '确定要删除吗？',
  'switch.open': '开启',
  'switch.close': '关闭',
  'submit.operate.success': '操作成功',
  'submit.create.success': '创建成功',
  'submit.update.success': '更新成功',
  'submit.delete.success': '删除成功',
  'menu.data': '平台数据',
  'menu.doc': '文件数据',
  'menu.star': '个人收藏',
  'menu.person': '人物数据',
  'menu.org': '机构数据',
  'menu.tag': '标签列表',
  'menu.subject': '事件数据',
  'menu.doc-detail': '文件详情',
  'menu.person-detail': '人物详情',
  'menu.org-detail': '机构详情',
  'menu.upload': '文件上传',
  'menu.work': '工作台',
  'menu.doc-edit': '编辑文件',
  'menu.person-edit': '编辑人物',
  'menu.subject-detail': '议题详情',
  ...localeSettings,
  ...localeLogin,
  ...localeWorkplace,
  ...localeLogLogin,
  ...localeSysMenu,
  ...localeIconPicker,
  ...localeLogOpera,
  ...localeSysDept,
  ...localeSysApi,
  ...localeServerMonitor,
  ...localeRedisMonitor,
  ...localeSysUser,
  ...localeSysRole,
  ...localDoc,
};
