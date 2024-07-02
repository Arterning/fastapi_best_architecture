<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.data'), $t('menu.doc')]" />
      <a-card :title="$t('menu.doc')" class="general-card">
        <a-row class="grid-demo" :gutter="{ md: 8, lg: 24, xl: 32 }">
          <a-col :span="8">
            <a-form
              :auto-label-width="true"
              :model="formModel"
              label-align="right"
            >
              <a-form-item field="title" :label="$t('关键字')">
                <a-input-tag
                  v-model="formModel.title"
                  :placeholder="$t('data.doc.columns.title.placeholder')"
                  @keyup.enter="search"
                  allow-clear
                >
                  <template #prefix>
                    <icon-search />
                  </template>
                  <template #suffix>
                    <icon-list class="searchModal" @click="searchModal" />
                  </template>
                </a-input-tag>
              </a-form-item>
            </a-form>
          </a-col>
          <a-col :span="8">
            <a-space :size="'large'">
              <a-upload
                :custom-request="customRequest"
                accept="application/pdf,application/zip"
                @before-upload="beforeUpload"
              />
            </a-space>
          </a-col>
        </a-row>
        <a-modal
          v-model:visible="visible"
          ok-text="搜索"
          cancel-text="重置"
          unmount-on-close
          @ok="search"
          @cancel="resetSelect"
        >
          <template #title> 详细搜索 </template>
          <a-form
            :auto-label-width="true"
            :model="formModel"
            label-align="right"
          >
            <a-row :gutter="16">
              <a-col :span="12">
                <a-form-item field="rangeValue" :label="$t('日期')">
                  <a-range-picker
                    v-model="formModel.rangeValue"
                    @keyup.enter="search"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item field="tags" :label="$t('标签')">
                  <a-select
                    v-model="formModel.tags"
                    placeholder="选择标签"
                    multiple
                    allow-clear
                  >
                    <a-option
                      v-for="item of allTags"
                      :key="item.id"
                      :value="item.id"
                      >{{ item.name }}</a-option
                    >
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-modal>
        <a-divider />
        <a-space :size="'medium'">
          <a-button type="primary" @click="NewApi()">
            <template #icon>
              <icon-plus />
            </template>
            {{ $t('admin.api.button.create') }}
          </a-button>
          <a-button
            :disabled="deleteButtonStatus()"
            status="danger"
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
            :columns="visibleColumns"
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
            <template #title="{ record }">
              <a-link
                @click="
                  $router.push({
                    name: 'DataDocDetail',
                    query: { docId: record.id },
                  })
                "
                >{{ record.title }}</a-link
              >
            </template>
            <template #tags="{ record }">
              <a-tag
                v-for="(tag, index) of record.tags"
                :key="index"
                checkable
                bordered
                >{{ tag.name }}
              </a-tag>
            </template>
            <template #operate="{ record }">
              <a-space>
                <a-link @click="FollowFile(record.id)">
                  {{ $t(`收藏`) }}
                </a-link>
                <a-link @click="EditApi(record.id)">
                  {{ $t(`admin.api.columns.edit`) }}
                </a-link>
              </a-space>
            </template>
          </a-table>
        </div>
        <div class="content-modal">
          <a-modal
            :visible="openAnalysis"
            :width="550"
            @ok="handleOk"
            @cancel="handleCancel"
          >
            <p>开始分析</p>
            <span v-for="text in analysisContent" :key="text">{{ text }}</span>
          </a-modal>
        </div>
        <div class="content-modal">
          <a-modal
            :closable="false"
            :on-before-ok="beforeSubmit"
            :title="drawerTitle"
            :visible="openNewOrEdit"
            :width="550"
            fullscreen
            @cancel="cancelReq"
            @ok="submitNewOrEdit"
          >
            <a-form ref="formRef" :model="form">
              <a-form-item
                :feedback="true"
                :label="$t('标题')"
                :rules="[{ required: true, message: $t('title') }]"
                field="title"
              >
                <a-input
                  v-model="form.title"
                  :placeholder="$t('标题')"
                ></a-input>
              </a-form-item>
              <a-form-item :label="$t('主题')" field="subject">
                <a-input v-model="form.subject"></a-input>
              </a-form-item>
              <a-form-item :label="$t('标签')" field="tags">
                <a-space wrap>
                  <a-tag
                    v-for="(tag, index) of tags"
                    :key="index"
                    :closable="index >= 0"
                    @close="handleRemove(tag)"
                  >
                    {{ tag }}
                  </a-tag>

                  <a-input
                    v-if="showInput"
                    ref="inputRef"
                    v-model.trim="inputVal"
                    :style="{ width: '90px' }"
                    size="mini"
                    @keyup.enter="handleAdd"
                    @blur="handleAdd"
                  />
                  <a-tag
                    v-else
                    :style="{
                      width: '90px',
                      backgroundColor: 'var(--color-fill-2)',
                      border: '1px dashed var(--color-fill-3)',
                      cursor: 'pointer',
                    }"
                    @click="handleEdit"
                  >
                    <template #icon>
                      <icon-plus />
                    </template>
                    Add Tag
                  </a-tag>
                </a-space>
              </a-form-item>
              <a-form-item :label="$t('内容')" field="content">
                <!-- <a-textarea
                  v-model="form.content"
                  :placeholder="$t('content')"
                  auto-size```````````````                                                                                              `
                ></a-textarea> -->
                <div class="markdown">
                  <MarkDown v-model="form.content"> </MarkDown>
                </div>
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
    RequestOption,
    TableColumnData,
    UploadRequest,
    Modal,
  } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import {
    computed,
    reactive,
    ref,
    nextTick,
    VueElement,
    onMounted,
  } from 'vue';
  import useLoading from '@/hooks/loading';
  import Footer from '@/components/footer/index.vue';
  import SettingTable from '@/components/SettingTable/index.vue';
  import {
    createDocApi,
    deleteDocApi,
    uploadDocApi,
    queryDocDetail,
    queryDocList,
    DocParams,
    DocReq,
    DocRes,
    updateDocApi,
    followDocApi,
  } from '@/api/doc';
  import { queryTagAll, TagRes } from '@/api/tag';
  import { Pagination } from '@/types/global';
  // 导入编辑器
  import MarkDown from '@/components/MarkDown/index.vue';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  // 搜索表单
  const generateFormModel = () => {
    return {
      title: undefined,
      time: undefined,
      location: undefined,
      rangeValue: ['', ''],
      tags: [],
    };
  };
  const formModel = ref(generateFormModel());

  // 弹框显示隐藏
  const visible = ref(false);

  const searchModal = () => {
    visible.value = true;
  };

  // 表格
  const renderData = ref<DocRes[]>([]);
  const operateRow = ref<number>(0);
  const rowSelectKeys = ref<number[]>([]);
  const rowSelection = reactive({
    showCheckedAll: true,
    selectedRowKeys: rowSelectKeys.value,
  });
  const basePagination: Pagination = {
    current: 1,
    defaultPageSize: 20,
    showTotal: true,
    showPageSize: true,
    bufferSize: 3,
  };
  const pagination: Pagination = reactive({
    ...basePagination,
  });

  const allTags = ref<TagRes[]>([]);


  const NewApi = () => {
    buttonStatus.value = 'new';
    drawerTitle.value = t('新建文件');
    resetForm(formDefaultValues);
    openNewOrEdit.value = true;
  };
  const EditApi = async (pk: number) => {
    buttonStatus.value = 'edit';
    operateRow.value = pk;
    drawerTitle.value = t('修改文件');
    const doc = await fetchApiDetail(pk);
    openNewOrEdit.value = true;

  };

  const FollowFile = async (id: number) => {
    await followDocApi(id);
    Message.success(t('submit.operate.success'));
  };

  const DeleteApi = () => {
    drawerTitle.value = t('删除文件');
    openDelete.value = true;
  };

  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('data.doc.columns.title'),
      dataIndex: 'title',
      slotName: 'title',
      width: 888,
      tooltip: true,
      ellipsis: true,
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: t('data.doc.columns.subject'),
      dataIndex: 'subject',
      slotName: 'subject',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
      tooltip: true,
      ellipsis: true,
    },
    {
      title: t('admin.api.columns.operate'),
      dataIndex: 'operate',
      slotName: 'operate',
      align: 'center',
      fixed: 'right',
      width: 160,
    },
  ]);
  // 列表展示
  const visibleColumns = ref<TableColumnData[]>([]);

  const updateVisibleColumns = (selectedColumns: string[]) => {
    visibleColumns.value = columns.value.filter((column) => {
      return column.dataIndex && selectedColumns.includes(column.dataIndex);
    });
  };

  const storageKey = "docTable";

  onMounted(() => {
    const savedColumns = localStorage.getItem(storageKey);
    if (savedColumns) {
      updateVisibleColumns(JSON.parse(savedColumns));
    } else {
      visibleColumns.value = columns.value; // 默认全部显示
    }
  });

  // 弹出分析窗口
  const openAnalysis = ref<boolean>(false);
  const analysisContent = ref<string[]>([]);

  const handleOk = () => {
    openAnalysis.value = false;
  };
  const handleCancel = () => {
    openAnalysis.value = false;
  };

  // 对话框
  const openNewOrEdit = ref<boolean>(false);
  const openDelete = ref<boolean>(false);
  const drawerTitle = ref<string>('');
  const cancelReq = () => {
    openNewOrEdit.value = false;
    openDelete.value = false;
  };
  const formDefaultValues: DocReq = {
    title: '',
    content: '',
    time: '',
    location: '',
    subject: '',
    source: '',
    persons: [],
    orgs: [],
    tags: [],
  };
  const form = reactive<DocReq>({ ...formDefaultValues });
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
        await createDocApi(form);
        cancelReq();
        Message.success(t('submit.create.success'));
        await fetchApiList();
      } else {
        await updateDocApi(operateRow.value, form);
        cancelReq();
        Message.success(t('submit.update.success'));
        await fetchApiList();
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
      await deleteDocApi({ pk: rowSelectKeys.value });
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

  // 请求API列表
  const fetchApiList = async (params: DocParams = {}) => {
    setLoading(true);
    try {
      const res = await queryDocList(params);
      renderData.value = res.items;
      pagination.total = res.total;
      pagination.current = params.page;
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
    fetchTagList();
  };

  // 获取Tag列表
  const fetchTagList = async () => {
    const res = await queryTagAll();
    allTags.value = res;
  };

  fetchApiList();

  // 请求部门详情
  const fetchApiDetail = async (pk: number) => {
    setLoading(true);
    try {
      const res = await queryDocDetail(pk);
      resetForm(res);
      return res;
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
    return null;
  };

  // 事件: 分页
  const onPageChange = async (current: number) => {
    await fetchApiList({
      page: current,
      size: pagination.pageSize,
      title: formModel.value.title,
    });
  };

  // 事件: 分页大小
  const onPageSizeChange = async (pageSize: number) => {
    pagination.pageSize = pageSize;
    await fetchApiList({ page: 1, size: pageSize });
  };

  // 搜索
  const search = async () => {
    await fetchApiList({
      ...formModel.value,
    } as unknown as DocParams);
  };

  // 重置
  const resetSelect = () => {
    formModel.value = generateFormModel();
  };

  // 重置方法
  const resetMethod = () => {
    formModel.value.title = undefined;
  };

  // 重置表单
  const resetForm = (data: Record<any, any>) => {
    Object.keys(data).forEach((key) => {
      // @ts-ignore
      form[key] = data[key];

      form.tags = data.tags.map((item: Record<any, any>) => item.name);

      if (form.tags) {
        tags.value = [...form.tags];
      }
    });
  };

  const beforeUpload = (file: File): Promise<boolean> => {
    return new Promise((resolve, reject) => {
      Modal.confirm({
        title: '确认上传',
        content: `确认上传 ${file.name}`,
        onOk: () => resolve(true),
        onCancel: () => reject(new Error('取消上传')),
      });
    });
  };

  const customRequest = (option: RequestOption): UploadRequest => {
    const { onProgress, onError, onSuccess, fileItem } = option;
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', fileItem.file as Blob);

    uploadDocApi(formData)
      .then((res) => {
        onSuccess(res);
        fetchApiList().then(() => {});
        Message.success(t('导入成功'));
      })
      .catch((error) => {
        onError(error);
        Message.success(t('导入失败'));
      });

    return {
      abort() {
        xhr.abort();
      },
    };
  };

  interface HasName {
    name: string;
  }

  const nameList = (objList: HasName[]) => {
    const nameList: string[] = [];
    objList.forEach((item) => {
      nameList.push(item.name);
    });
    return nameList;
  };


  const tags = ref<string[]>([]);
  const inputRef = ref<HTMLInputElement>();
  const showInput = ref(false);
  const inputVal = ref('');

  const handleEdit = () => {
    showInput.value = true;

    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus();
      }
    });
  };

  const handleAdd = () => {
    if (inputVal.value) {
      tags.value.push(inputVal.value);
      form.tags?.push(inputVal.value);
      inputVal.value = '';
    }
    showInput.value = false;
  };

  const handleRemove = (key: string) => {
    tags.value = tags.value.filter((tag) => tag !== key);
    form.tags = form.tags?.filter((tag) => tag !== key);
  };
</script>

<script lang="ts">
  export default {
    name: 'Doc',
  };
</script>

<style lang="less" scoped>
  .content {
    padding-top: 20px;
  }
  .searchModal {
    cursor: pointer;
  }
  // .markdown {
  //   width: 500px;
  //   height: 600px;
  // }
</style>
