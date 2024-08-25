<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.data'), $t('机构管理')]" />
      <a-card :title="$t('机构管理')" class="general-card">
        <a-row>
          <a-col :flex="62">
            <a-form
              :auto-label-width="true"
              :model="formModel"
              label-align="right"
            >
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-form-item :label="$t('组织名')" field="name">
                    <a-input
                      v-model="formModel.name"
                      :placeholder="$t('组织名搜索')"
                      @keyup.enter="search"
                    />
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item :label="$t('文件名')" field="docs">
                    <a-select
                      v-model="formModel.docs"
                      :style="{ width: '320px' }"
                      :loading="docsLoading"
                      placeholder="文件名搜索"
                      multiple
                      @search="handleDocSearch"
                    >
                      <a-option
                        v-for="item of docOptions"
                        :key="item.value"
                        :value="item.value"
                        >{{ item.label }}
                      </a-option>
                    </a-select>
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form>
          </a-col>
          <a-divider direction="vertical" style="height: 30px" />
          <a-col :span="6">
            <a-space :size="'medium'" direction="horizontal">
              <a-button type="primary" @click="search">
                <template #icon>
                  <icon-search />
                </template>
                {{ $t('admin.api.form.search') }}
              </a-button>
              <a-button @click="resetSelect">
                <template #icon>
                  <icon-refresh />
                </template>
                {{ $t('admin.api.form.reset') }}
              </a-button>
            </a-space>
          </a-col>
        </a-row>
        <a-space :size="'medium'">
          <a-button type="outline" shape="round" @click="NewApi()">
            <template #icon>
              <icon-plus />
            </template>
            {{ $t('admin.api.button.create') }}
          </a-button>
          <a-button v-if="!!formModel.name" @click="expand">
            {{ $t('展开/收起') }}
          </a-button>
          <a-button
            :disabled="deleteButtonStatus()"
            status="danger"
            shape="round"
            @click="DeleteApi"
          >
            <template #icon>
              <icon-minus />
            </template>
            {{ $t('admin.api.button.delete') }}
          </a-button>
          <SettingTable
            :columns="columns"
            :storageKey="storageKey"
            @update-columns="updateVisibleColumns"
          />
        </a-space>
        <div class="content">
          <a-table
            ref="tableRef"
            v-model:selected-keys="rowSelectKeys"
            :bordered="{cell:true}"
            :pagination="false"
            :columns="(visibleColumns as TableColumnData[])"
            :data="renderData"
            :loading="loading"
            :row-selection="rowSelection"
            :size="'medium'"
            row-key="id"
            column-resizable
          >
            <template #index="{ rowIndex }">
              {{ rowIndex + 1 }}
            </template>
            <template #name="{ record }">
              <a-link @click="handleClickDetail(record.id)">{{
                record.name
              }}</a-link>
            </template>
            <template #start_date="{ record }">
              {{ convertDateStr(record.start_date) }}
            </template>
            <template #operate="{ record }">
              <a-space>
                <a-link @click="EditApi(record.id)">
                  {{ $t(`admin.api.columns.edit`) }}
                </a-link>
              </a-space>
            </template>
          </a-table>
        </div>
        <div class="content-modal">
          <a-modal
            :closable="false"
            :on-before-ok="beforeSubmit"
            :title="drawerTitle"
            :visible="openNewOrEdit"
            :width="850"
            @cancel="cancelReq"
            @ok="submitNewOrEdit"
          >
            <a-form ref="formRef" :model="form">
              <a-form-item
                :feedback="true"
                :label="$t('组织名')"
                :rules="[{ required: true, message: $t('组织名不能为空') }]"
                field="name"
              >
                <a-input
                  v-model="form.name"
                  :placeholder="$t('请输入组织名')"
                ></a-input>
              </a-form-item>
              <a-form-item
                :feedback="true"
                :label="$t('上级组织')"
                field="parent_id"
              >
                <a-select
                  v-model="form.parent_id"
                  :loading="orgLoading"
                  placeholder="选择上级组织"
                  allow-clear
                  allow-search
                  @search="handleOrgSearch"
                >
                  <a-option
                    v-for="item of orgOptions"
                    :key="item.value"
                    :value="item.value"
                    >{{ item.label }}</a-option
                  >
                </a-select>
              </a-form-item>

              <a-form-item
                :feedback="true"
                :label="$t('组织详情')"
                field="detail"
              >
                <a-textarea
                  v-model="form.detail"
                  :placeholder="$t('请输入组织详情')"
                ></a-textarea>
              </a-form-item>

              <a-form-item field="persons" :label="$t('关联人物')">
                <a-select
                  v-model="form.persons"
                  :loading="personLoading"
                  placeholder="选择人物"
                  multiple
                  @search="handlePersonSearch"
                >
                  <a-option
                    v-for="item of personOptions"
                    :key="item.value"
                    :value="item.value"
                    >{{ item.label }}</a-option
                  >
                </a-select>
              </a-form-item>
              
              <a-form-item
                :feedback="true"
                :label="$t('关联文件')"
                field="docs"
              >
                <a-select
                  v-model="form.docs"
                  :loading="docsLoading"
                  placeholder="选择文件"
                  multiple
                  allow-clear
                  allow-search
                  @search="handleDocSearch"
                >
                  <a-option
                    v-for="item of docOptions"
                    :key="item.value"
                    :value="item.value"
                    >{{ item.label }}
                  </a-option>
                </a-select>
              </a-form-item>
              
              <a-form-item
                :feedback="true"
                :label="$t('默认展示')"
                field="detail"
              >
                <a-switch
                  v-model="form.default_show"
                ></a-switch>
              </a-form-item>
            </a-form>
          </a-modal>
          <a-modal
            :closable="false"
            :title="`${$t('modal.title.tips')}`"
            :visible="openDelete"
            :width="360"
            @cancel="cancelReq"
            @ok="submitDelete"
          >
            <a-space>
              <icon-exclamation-circle-fill size="24" style="color: #e6a23c" />
              {{ $t('modal.title.tips.delete') }}
            </a-space>
          </a-modal>
        </div>
      </a-card>
    </a-layout>
  </div>
  <div class="footer">
    <Footer />
  </div>
</template>

<script lang="ts" setup>
  import {
    Message,
    TableColumnData,
    TreeFieldNames,
  } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import { computed, reactive, ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import useLoading from '@/hooks/loading';
  import Footer from '@/components/footer/index.vue';
  import SettingTable from '@/components/SettingTable/index.vue';

  import {
    createOrgApi,
    deleteOrgApi,
    queryOrgDetail,
    OrgParams,
    OrgReq,
    updateOrgApi,
    queryOrgTree,
    OrgTreeRes,
    queryOrgAll,
    OrgRes,
  } from '@/api/org';
  import { DocRes, queryDocAll, queryDocList } from '@/api/doc';
  import { treeSelectDataType } from '@/types/global';
  import { PersonRes, queryPersonAll, queryPersonList } from '@/api/person';
  import { convertDateStr } from '@/utils/string';
  import {useDocStore} from "@/store";
  import router from '@/router';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  interface FormModel {
    name: string | undefined;
    location: string | undefined;
    start_date: Date | undefined;
    detail: string | undefined;
    parent_id: number | undefined;
    docs: number[];
  }
  // 表单
  const generateFormModel = (): FormModel => {
    return {
      name: undefined,
      location: undefined,
      start_date: undefined,
      detail: undefined,
      parent_id: undefined,
      docs: [],
    };
  };
  const formModel = ref(generateFormModel());
  // 表格
  const renderData = ref<OrgTreeRes[]>([]);
  const operateRow = ref<number>(0);
  const rowSelectKeys = ref<number[]>([]);
  const rowSelection = reactive({
    showCheckedAll: true,
    selectedRowKeys: rowSelectKeys.value,
  });

  const docsLoading = ref(false);

  const docs = ref<DocRes[]>([]);
  const docOptions = computed(() => {
    return docs.value.map((item) => {
      return {
        value: item.id,
        label: item.title,
      };
    });
  });

  const route = useRoute();
  const { docId, docName } = route.query;
  const docIdNumber = Number(docId);
  const docNameString = docName as string;
  if (docId) {
    formModel.value.docs.push(docIdNumber);
    docs.value.push({
      id: docIdNumber,
      title: docNameString,
    });
  }

  const NewApi = () => {
    buttonStatus.value = 'new';
    drawerTitle.value = t('新建组织');
    resetForm(formDefaultValues);
    openNewOrEdit.value = true;
  };
  const EditApi = async (pk: number) => {
    buttonStatus.value = 'edit';
    operateRow.value = pk;
    drawerTitle.value = t('编辑组织');
    const org = await fetchApiDetail(pk);
    openNewOrEdit.value = true;

    // 初始化文档选择数据
    if (org && org.docs) {
      docs.value = [...org.docs];
    }

    if (docs.value.length === 0) {
      const docList = await queryDocList({});
      docs.value = docList.items;
    }

    // 初始化人物选择数据
    if (org && org.persons) {
      persons.value = [...org.persons];
    }

    if (persons.value.length === 0) {
      const personList = await queryPersonList({});
      persons.value = personList.items;
    }

    // 初始化组织选择框
    if (orgs.value.length === 0) {
      orgs.value = await queryOrgAll({});
    }

    if (org && org.parent) {
        orgs.value.push(org.parent);
    }
  };
  const DeleteApi = () => {
    drawerTitle.value = t('admin.api.columns.delete.drawer');
    openDelete.value = true;
  };
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('组织名'),
      dataIndex: 'name',
      slotName: 'name',
      width: 500,
      tooltip: true,
      ellipsis: true,
    },
    {
      title: t('admin.api.columns.operate'),
      dataIndex: 'operate',
      slotName: 'operate',
      align: 'center',
    },
  ]);

  // 列表展示

  const visibleColumns = ref<TableColumnData[]>([]);

  const updateVisibleColumns = (selectedColumns: string[]) => {
    visibleColumns.value = columns.value.filter((column) => {
      return column.dataIndex && selectedColumns.includes(column.dataIndex);
    });
  };

  const storageKey = "orgTable";
  onMounted(() => {
    const savedColumns = localStorage.getItem(storageKey);
    if (savedColumns) {
      updateVisibleColumns(JSON.parse(savedColumns));
    } else {
      visibleColumns.value = columns.value; // 默认全部显示
    }
  });

  // 对话框
  const openNewOrEdit = ref<boolean>(false);
  const openDelete = ref<boolean>(false);
  const drawerTitle = ref<string>('');
  const cancelReq = () => {
    openNewOrEdit.value = false;
    openDelete.value = false;
    docs.value = [];
  };
  const formDefaultValues: OrgReq = {
    name: '',
    detail: '',
    docs: [],
    persons: [],
  };
  const form = reactive<OrgReq>({ ...formDefaultValues });
  const buttonStatus = ref<string>();
  const formRef = ref();

  // 表单校验
  const beforeSubmit = async (done: any) => {
    const res = await formRef.value?.validate();
    if (!res) {
      // 关闭对话框
      done(true);
    }
    done(false);
  };

  // 提交按钮
  const submitNewOrEdit = async () => {
    setLoading(true);
    try {
      if (buttonStatus.value === 'new') {
        await createOrgApi(form);
        cancelReq();
        Message.success(t('submit.create.success'));
        // await fetchApiList();
      } else {
        await updateOrgApi(operateRow.value, form);
        cancelReq();
        Message.success(t('submit.update.success'));
        // await fetchApiList();
      }
    } catch (error) {
      // console.log(error);
    } finally {
      setLoading(false);
    }
  };

  // 删除按钮状态
  const deleteButtonStatus = () => {
    return rowSelectKeys.value?.length === 0;
  };

  // 删除按钮
  const submitDelete = async () => {
    setLoading(true);
    try {
      await deleteOrgApi({ pk: rowSelectKeys.value });
      cancelReq();
      Message.success(t('submit.delete.success'));
      await fetchApiList();
      rowSelectKeys.value = [];
    } catch (error) {
      openDelete.value = false;
      // console.log(error);
    } finally {
      openDelete.value = false;
      setLoading(false);
    }
  };

  // 转换菜单数据结构
  const transformDeptData = (data: OrgTreeRes[]) => {
    const result: treeSelectDataType[] = [
      {
        id: null,
        name: '顶级',
        disabled: true,
        children: [],
      },
    ];
    data.forEach((item) => {
      result[0].children.push(item);
    });
    return result;
  };

  // 请求API列表
  const fetchApiList = async (params: OrgParams = {}) => {
    setLoading(true);
    try {
      const res = await queryOrgTree(params);
      renderData.value = res;
      treeSelectData.value = transformDeptData(res);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const docStore = useDocStore();

  formModel.value = {
    ...formModel.value,
    name: docStore.orgQuery,
  };

  fetchApiList({
    ...formModel.value,
  });

  // 请求部门详情
  const fetchApiDetail = async (pk: number) => {
    setLoading(true);
    try {
      const res = await queryOrgDetail(pk);
      resetForm(res);
      return res;
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
    return null;
  };

  // 搜索
  const search = async () => {

    // 如果展开了 并且 搜索内容为空 则收起
    if (expandAll.value && !formModel.value.name) {
      expand();
    }

    await fetchApiList({
      ...formModel.value,
    } as unknown as OrgParams);


    // 如果没有展开 并且 搜索内容不为空 则展开
    if (!expandAll.value && !!formModel.value.name) {
      expand();
    }

    docStore.setState({
      orgQuery: formModel.value.name,
    });

  };

  // 重置
  const resetSelect = () => {
    formModel.value = generateFormModel();
  };

  // 重置方法
  const resetMethod = () => {
    formModel.value.name = undefined;
  };

  // 重置表单
  const resetForm = (data: Record<any, any>) => {
    Object.keys(data).forEach((key) => {
      // @ts-ignore
      form[key] = data[key];

      form.docs = data.docs.map((item: Record<any, any>) => item.id);
      form.persons = data.persons.map((item: Record<any, any>) => item.id);
      form.parent_id = data.parent?.id;
    });
  };

  const handleDocSearch = async (value: string) => {
    if (value) {
      docsLoading.value = true;

      const search = await queryDocAll({
        title: [value],
      });

      if(search) {
        search.forEach((s) => {
          if (!docs.value.find((p => p.id === s.id))) {
            docs.value.push(s);
          }
        });
      }

      docsLoading.value = false;
    } else {
      // docs.value = [];
    }
  };

  const treeSelectData = ref();

  const tableRef = ref();
  const expandAll = ref<boolean>(false);
  // 展开/收起
  const expand = () => {
    expandAll.value = !expandAll.value;
    tableRef.value?.expandAll(expandAll.value);
  };

  const orgs = ref<OrgRes[]>([]);
  const orgOptions = computed(() => {
    return orgs.value.map((item) => {
      return {
        value: item.id,
        label: item.name,
      };
    });
  });
  const orgLoading = ref(false);
  const handleOrgSearch = async (value: string) => {
    if (value) {
      orgLoading.value = true;

      const search = await queryOrgAll({
        name: value,
      });

      if (search) {
        search.forEach((s) => {
          if (!orgs.value.find((p => p.id === s.id))) {
            orgs.value.push(s);
          }
        });
      }

      orgLoading.value = false;
    } else {
      // orgs.value = [];
    }
  };

  const persons = ref<PersonRes[]>([]);
  const personOptions = computed(() => {
    return persons.value.map((item) => {
      return {
        value: item.id,
        label: item.name,
      };
    });
  });
  const personLoading = ref(false);
  const handlePersonSearch = async (value: string) => {
    if (value) {
      personLoading.value = true;

      const search = await queryPersonAll({
        name: value,
      });
      
      if (search) {
        search.forEach((s) => {
          if (!persons.value.find((p => p.id === s.id))) {
            persons.value.push(s);
          }
        });
      }

      personLoading.value = false;
    } else {
      // persons.value = [];
    }
  };

  const handleClickDetail = (id: number) => {
    router.push({
      path: '/data/org-detail',
      query: {
        orgId: id,
      },
    })
  };
</script>

<script lang="ts">
  export default {
    name: 'OrgApi',
  };
</script>

<style lang="less" scoped>
  .content {
    padding-top: 20px;
  }
</style>
