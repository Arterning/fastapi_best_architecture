<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.data'), $t('事件数据')]" />
      <a-card :title="$t('事件数据')" class="general-card">
        <a-row>
          <a-col :flex="62">
            <a-form
              :auto-label-width="true"
              :model="formModel"
              label-align="right"
            >
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-form-item :label="$t('议题名')" field="name">
                    <a-input
                      v-model="formModel.name"
                      :placeholder="$t('议题名搜索')"
                      @keyup.enter="search"
                    />
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
            v-model:selected-keys="rowSelectKeys"
            :bordered="{ cell: true }"
            :columns="(visibleColumns as TableColumnData[])"
            :data="renderData"
            :loading="loading"
            :pagination="pagination"
            :row-selection="rowSelection"
            :size="'medium'"
            row-key="id"
            column-resizable
            @page-change="onPageChange"
            @page-size-change="onPageSizeChange"
          >
            <template #index="{ rowIndex }">
              {{ rowIndex + 1 }}
            </template>
            <template #name="{ record }">
              <a-link
                @click="
                  $router.push({
                    name: 'DataSubjectDetail',
                    query: { subjectId: record.id },
                  })
                "
                >{{ record.name }}</a-link
              >
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
            :width="550"
            @cancel="cancelReq"
            @ok="submitNewOrEdit"
          >
            <a-form ref="formRef" :model="form">
              <a-form-item
                :feedback="true"
                :label="$t('议题名')"
                :rules="[{ required: true, message: $t('议题名不能为空') }]"
                field="name"
              >
                <a-input
                  v-model="form.name"
                  :placeholder="$t('请输入议题名')"
                ></a-input>
              </a-form-item>
              <a-form-item
                :feedback="true"
                :label="$t('议题类型')"
                field="detail"
              >
                <a-textarea
                  v-model="form.type"
                  :placeholder="$t('请输入议题类型')"
                ></a-textarea>
              </a-form-item>
              <a-form-item
                :feedback="true"
                :label="$t('议题详情')"
                field="detail"
              >
                <a-textarea
                  v-model="form.detail"
                  :placeholder="$t('请输入议题详情')"
                ></a-textarea>
              </a-form-item>
              <a-form-item
                :feedback="true"
                :label="$t('议题文件')"
                field="docs"
              >
                <a-select
                  v-model="form.docs"
                  :loading="docsLoading"
                  placeholder="选择议题文件"
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

              <a-form-item :label="$t('关联人物')" field="persons">
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

              <a-form-item :label="$t('关联组织')" field="orgs">
                <a-select
                  v-model="form.orgs"
                  :loading="orgLoading"
                  placeholder="选择组织"
                  multiple
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

              <a-form-item :label="$t('议题脉络')">
                <a-space direction="vertical">
                  <a-button type="primary" @click="addHis"
                    >添加</a-button
                  >
                  <div v-for="item of form.his" :key="item.index">
                    <a-space direction="horizontal">
                      <a-input
                        v-model="item.title"
                        placeholder="标题"
                      ></a-input>
                      <a-textarea
                        v-model="item.detail"
                        placeholder="详情"
                      ></a-textarea>
                      <a-button @click="deleteHis(item.index)"
                        >删除</a-button
                      >
                    </a-space>
                  </div>
                </a-space>
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
  import { Message, TableColumnData } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import { computed, reactive, ref, onMounted } from 'vue';
  import SettingTable from '@/components/SettingTable/index.vue';
  import useLoading from '@/hooks/loading';
  import Footer from '@/components/footer/index.vue';
  import {
    createSubjectApi,
    deleteSubjectApi,
    querySubjectDetail,
    querySubjectList,
    SubjectParams,
    SubjectReq,
    SubjectRes,
    updateSubjectApi,
  } from '@/api/subject';
  import { Pagination } from '@/types/global';
  import { DocRes, queryDocAll, queryDocList } from '@/api/doc';
  import { PersonRes, queryPersonAll } from '@/api/person';
  import { OrgRes, queryOrgAll } from '@/api/org';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  // 表单
  const generateFormModel = () => {
    return {
      name: undefined,
      detail: undefined,
      his: []
    };
  };
  const formModel = ref(generateFormModel());
  // 表格
  const renderData = ref<SubjectRes[]>([]);
  const operateRow = ref<number>(0);
  const rowSelectKeys = ref<number[]>([]);
  const rowSelection = reactive({
    showCheckedAll: true,
    selectedRowKeys: rowSelectKeys.value,
  });
  const pagination: Pagination = reactive({
    current: 1,
    defaultPageSize: 10,
    pageSize: 10,
    showTotal: true,
    showPageSize: true,
    bufferSize: 3,
  });
  const NewApi = () => {
    buttonStatus.value = 'new';
    drawerTitle.value = t('新增议题');
    resetForm(formDefaultValues);
    openNewOrEdit.value = true;
  };
  const EditApi = async (pk: number) => {
    buttonStatus.value = 'edit';
    operateRow.value = pk;
    drawerTitle.value = t('编辑议题');
    const subject = await fetchApiDetail(pk);
    openNewOrEdit.value = true;

    // 初始化文档选择数据
    if (subject && subject.docs) {
      docs.value = [...subject.docs];
    }

    if (docs.value.length === 0) {
      const docList = await queryDocList({});
      docs.value = docList.items;
    }
  };
  const DeleteApi = () => {
    drawerTitle.value = t('admin.api.columns.delete.drawer');
    openDelete.value = true;
  };
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('议题名'),
      dataIndex: 'name',
      slotName: 'name',
      tooltip: true,
      ellipsis: true,
    },
    {
      title: t('议题类型'),
      dataIndex: 'type',
      slotName: 'type',
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

  const storageKey = 'subjectTable';
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
  };
  const formDefaultValues: SubjectReq = {
    name: '',
    type: '',
    detail: '',
    docs: [],
    persons: [],
    orgs: [],
    his: [],
  };
  const form = reactive<SubjectReq>({ ...formDefaultValues });
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
        await createSubjectApi(form);
        cancelReq();
        Message.success(t('submit.create.success'));
        await fetchApiList({ ...formModel.value, size: pagination.pageSize });
      } else {
        await updateSubjectApi(operateRow.value, form);
        cancelReq();
        Message.success(t('submit.update.success'));
        await fetchApiList({ ...formModel.value, size: pagination.pageSize });
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
      await deleteSubjectApi({ pk: rowSelectKeys.value });
      cancelReq();
      Message.success(t('submit.delete.success'));
      await fetchApiList({ ...formModel.value, size: pagination.pageSize });
      rowSelectKeys.value = [];
    } catch (error) {
      openDelete.value = false;
      // console.log(error);
    } finally {
      openDelete.value = false;
      setLoading(false);
    }
  };

  // 请求API列表
  const fetchApiList = async (params: SubjectParams = {}) => {
    setLoading(true);
    try {
      const res = await querySubjectList(params);
      renderData.value = res.items;
      pagination.total = res.total;
      pagination.current = params.page;
    } catch (error) {
      // console.log(error);
    } finally {
      setLoading(false);
    }
  };
  fetchApiList({ ...formModel.value, size: pagination.pageSize });

  // 请求部门详情
  const fetchApiDetail = async (pk: number) => {
    setLoading(true);
    try {
      const res = await querySubjectDetail(pk);
      resetForm(res);

      if (res?.persons) {
        persons.value = [...res.persons];
      }

      if (res?.orgs) {
        orgs.value = [...res.orgs];
      }
      return res;
    } catch (error) {
      console.log(error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // 事件: 分页
  const onPageChange = async (current: number) => {
    await fetchApiList({
      ...formModel.value,
      page: current,
      size: pagination.pageSize,
    });
  };

  // 事件: 分页大小
  const onPageSizeChange = async (pageSize: number) => {
    pagination.pageSize = pageSize;
    await fetchApiList({ ...formModel.value, page: 1, size: pageSize });
  };

  // 搜索
  const search = async () => {
    await fetchApiList({
      ...formModel.value,
      size: pagination.pageSize,
    } as unknown as SubjectParams);
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
      form.orgs = data.orgs.map((item: Record<any, any>) => item.id);
    });
  };

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


  const addHis = () => {
    const index = form.his.length;
    const { his } = form;
    his.push({ index, title: '', detail: '' });
  };

  const deleteHis = (index: number) => {
    const { his } = form;
    his.splice(index, 1);
    // eslint-disable-next-line
    for (let i = 0; i < his.length; i++) {
      his[i].index = i;
    }
  };
</script>

<script lang="ts">
  export default {
    name: 'SubjectApi',
  };
</script>

<style lang="less" scoped>
  .content {
    padding-top: 20px;
  }
</style>
