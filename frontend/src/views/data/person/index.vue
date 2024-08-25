<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.data'), $t('人物管理')]" />
      <a-card :title="$t('人物管理')" class="general-card">
        <a-row>
          <a-col :flex="62">
            <a-form
              :auto-label-width="true"
              :model="formModel"
              label-align="right"
            >
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-form-item :label="$t('人物名')" field="name">
                    <a-input
                      v-model="formModel.name"
                      :placeholder="$t('人物名搜索')"
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
            :bordered="{cell:true}"
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
            <template #sex="{ record }">
              {{ getSexLabel(record.sex) }}
            </template>
            <template #name="{ record }">
              <a-link
                @click="
                  $router.push({
                    name: 'DataPersonDetail',
                    query: { personId: record.id },
                  })
                "
                >{{ record.name }}</a-link
              >
            </template>
          </a-table>
        </div>
        <div class="content-modal">
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
  import { useRoute } from 'vue-router';
  import useLoading from '@/hooks/loading';
  import Footer from '@/components/footer/index.vue';
  import SettingTable from '@/components/SettingTable/index.vue';
  import {
    deletePersonApi,
    queryPersonList,
    PersonParams,
    PersonRes,
  } from '@/api/person';
  import { Pagination } from '@/types/global';
  import { DocRes, queryDocAll } from '@/api/doc';
  import { useDocStore } from '@/store';
  import router from '@/router';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  interface FormModel {
    name: string | undefined;
    job: string | undefined;
    detail: string | undefined;
    docs: number[];
  }
  // 列表展示

  const visibleColumns = ref<TableColumnData[]>([]);

  const updateVisibleColumns = (selectedColumns: string[]) => {
    visibleColumns.value = columns.value.filter((column) => {
      return column.dataIndex && selectedColumns.includes(column.dataIndex);
    });
  };

  const storageKey = 'personTable';
  onMounted(() => {
    const savedColumns = localStorage.getItem(storageKey);
    if (savedColumns) {
      updateVisibleColumns(JSON.parse(savedColumns));
    } else {
      visibleColumns.value = columns.value; // 默认全部显示
    }
  });

  // 表单
  const generateFormModel = (): FormModel => {
    return {
      name: undefined,
      detail: undefined,
      job: undefined,
      docs: [],
    };
  };
  const formModel = ref(generateFormModel());
  // 表格
  const renderData = ref<PersonRes[]>([]);
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

  const handleDocSearch = async (value: string) => {
    if (value) {
      docsLoading.value = true;

      docs.value = await queryDocAll({
        title: [value],
      });

      docsLoading.value = false;
    } else {
      docs.value = [];
    }
  };

  const sexOptions = [
    {
      value: 1,
      label: '男',
    },
    {
      value: 0,
      label: '女',
    },
  ];

  const getSexLabel = (value: number) => {
    const sex = sexOptions.find((item) => item.value === value);

    if (sex) {
      return sex.label;
    }

    return '';
  };


  const NewApi = () => {
    router.push({
      name: 'DataPersonEdit',
    });
  };
  
  const DeleteApi = () => {
    drawerTitle.value = t('admin.api.columns.delete.drawer');
    openDelete.value = true;
  };
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('人物名'),
      dataIndex: 'name',
      slotName: 'name',
      tooltip: true,
      ellipsis: true,
    },
  ]);

  // 对话框
  const openNewOrEdit = ref<boolean>(false);
  const openDelete = ref<boolean>(false);
  const drawerTitle = ref<string>('');
  const cancelReq = () => {
    openNewOrEdit.value = false;
    openDelete.value = false;
    docs.value = [];
  };

  // 删除按钮状态
  const deleteButtonStatus = () => {
    return rowSelectKeys.value?.length === 0;
  };

  // 删除按钮
  const submitDelete = async () => {
    setLoading(true);
    try {
      await deletePersonApi({ pk: rowSelectKeys.value });
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
  const fetchApiList = async (params: PersonParams = {}) => {
    setLoading(true);
    try {
      const res = await queryPersonList(params);
      renderData.value = res.items;
      pagination.total = res.total;
      pagination.current = params.page;
    } catch (error) {
      // console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const docStore = useDocStore();

  formModel.value = {
    ...formModel.value,
    name: docStore.personQuery,
  };

  fetchApiList({
    ...formModel.value,
    size: pagination.pageSize,
  });

  // 事件: 分页
  const onPageChange = async (current: number) => {
    await fetchApiList({
      page: current,
      size: pagination.pageSize,
      ...formModel.value,
    });
  };

  // 事件: 分页大小
  const onPageSizeChange = async (pageSize: number) => {
    pagination.pageSize = pageSize;
    await fetchApiList({ page: 1, size: pageSize, ...formModel.value });
  };

  // 搜索
  const search = async () => {
    await fetchApiList({
      ...formModel.value,
      size: pagination.pageSize,
    } as unknown as PersonParams);
    docStore.setState({
      personQuery: formModel.value.name,
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

</script>

<script lang="ts">
  export default {
    name: 'PersonApi',
  };
</script>

<style lang="less" scoped>
  .content {
    padding-top: 20px;
  }
</style>
