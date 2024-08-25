<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card :title="$t('编辑人物')" class="general-card">
        <a-space direction="vertical" size="large" :style="{ width: '80%' }">
          <a-form ref="formRef" :model="form">
            <a-form-item
              :feedback="true"
              :label="$t('人物照片')"
              field="avator"
            >
              <a-upload
                list-type="picture-card"
                :custom-request="customRequest"
                :on-before-remove="onBeforeRemove"
                v-model:file-list="fileList"
                image-preview
              />
            </a-form-item>
            <a-form-item
              :feedback="true"
              :label="$t('人物名')"
              :rules="[{ required: true, message: $t('人物名不能为空') }]"
              field="name"
            >
              <a-input
                v-model="form.name"
                :placeholder="$t('请输入人物名')"
              ></a-input>
            </a-form-item>
            
            <a-form-item :feedback="true" :label="$t('关联组织')" field="orgs">
              <a-select
                v-model="form.orgs"
                :loading="orgsLoading"
                placeholder="选择关联组织"
                multiple
                @search="handleOrgSearch"
              >
                <a-option
                  v-for="item of orgOptions"
                  :key="item.value"
                  :value="item.value"
                  >{{ item.label }}
                </a-option>
              </a-select>
            </a-form-item>
            <a-form-item :feedback="true" :label="$t('关联文件')" field="docs">
              <a-select
                v-model="form.docs"
                :loading="docsLoading"
                placeholder="选择关联文件"
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

            <a-form-item
              :feedback="true"
              :label="$t('人物简历')"
              field="detail"
            >
              <a-textarea
                v-model="form.detail"
                :placeholder="$t('请输入人物简历')"
              ></a-textarea>
            </a-form-item>

            <a-form-item :label="$t('人物关系')">
              <a-space direction="vertical">
                <a-button type="primary" @click="addPersonRelation"
                  >添加</a-button
                >
                <div v-for="item of form.relations" :key="item.index">
                  <a-space direction="horizontal">
                    <a-select
                      :loading="personLoading"
                      allow-search
                      v-model="item.other_id"
                      placeholder="选择人物"
                      @search="handlePersonSearch"
                    >
                      <a-option
                        v-for="item of personOptions"
                        :key="item.value"
                        :value="item.value"
                        >{{ item.label }}</a-option
                      >
                    </a-select>
                    <a-input
                      v-model="item.detail"
                      placeholder="请输入人物关系"
                    ></a-input>
                    <a-button @click="deletePersonRelation(item.index)"
                      >删除</a-button
                    >
                  </a-space>
                </div>
              </a-space>
            </a-form-item>

            <a-form-item>
              <a-button type="primary" :loading="loading" @click="handleSubmit"
                >保存</a-button
              >
              <a-button style="margin-left: 10px" @click="handleCancel"
                >取消</a-button
              >
            </a-form-item>
          </a-form>
        </a-space>
      </a-card>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
  import { useRoute } from 'vue-router';
  import { FileItem, Message, RequestOption, TableColumnData, UploadRequest } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import { computed, reactive, ref, onMounted } from 'vue';
  import useLoading from '@/hooks/loading';
  import Footer from '@/components/footer/index.vue';
  import SettingTable from '@/components/SettingTable/index.vue';
  import {
    createPersonApi,
    deletePersonApi,
    queryPersonDetail,
    queryPersonList,
    PersonParams,
    PersonReq,
    PersonRes,
    updatePersonApi,
    queryPersonAll,
  } from '@/api/person';
  import { DocRes, queryDocAll, queryDocList } from '@/api/doc';
  import { OrgRes, queryOrgAll, queryOrgList } from '@/api/org';
  import Breadcrumb from '@/components/link-breadcrumb/index.vue';
  import router from '@/router';
  import { getToken } from '@/utils/auth';
  import { getPreviewURL } from '@/utils/image';

  const { t } = useI18n();
  const formRef = ref();
  const { loading, setLoading } = useLoading(false);


  const fetchData = async (personId: number) => {
    setLoading(true);
    try {
      const res = await queryPersonDetail(personId);
      resetForm(res);

      if (res?.docs) {
        docs.value = [...res.docs];
      }

      if (res?.orgs) {
        orgs.value = [...res.orgs];
      }
      if (res?.persons) {
        persons.value = [...res.persons];
      }

      if (res?.attachments) {
        fileList.value = res.attachments.map((item: Record<string, any>) => {
          return {
            uid: item.id,
            name: item.name,
            url: getPreviewURL(item.obj_name),
          }
        })
      }
      
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 重置表单
  const resetForm = (data: Record<any, any>) => {
    Object.keys(data).forEach((key) => {
      // @ts-ignore
      form[key] = data[key];

      form.docs = data.docs.map((item: Record<any, any>) => item.id);
      form.orgs = data.orgs.map((item: Record<any, any>) => item.id);
    });
  };

  const route = useRoute();
  const { personId } = route.query;
  const personIdNumber = Number(personId);
  if (personIdNumber) {
    fetchData(personIdNumber);
  }

  const formDefaultValues: PersonReq = {
    name: '',
    sex: 1,
    job: '',
    nation: '',
    country: '',
    birth_addr: '',
    birth_date: undefined,
    detail: '',
    docs: [],
    orgs: [],
    persons: [],
    attachments: [],
    relations: [],
  };
  const form = reactive<PersonReq>({ ...formDefaultValues });

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

  const orgsLoading = ref(false);
  const orgs = ref<OrgRes[]>([]);
  const orgOptions = computed(() => {
    return orgs.value.map((item) => {
      return {
        value: item.id,
        label: item.name,
      };
    });
  });
  const handleOrgSearch = async (value: string) => {
    if (value) {
      orgsLoading.value = true;

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

      orgsLoading.value = false;
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

  const routes = [
    {
      path: '/data/person',
      label: '人物管理',
    },
    {
      path: `/data/person-edit?personId=${personIdNumber}`,
      label: '编辑人物',
    },
  ];

  const addPersonRelation = () => {
    const index = form.relations.length;
    const { relations } = form;
    relations.push({ index, other_id: undefined, detail: undefined });
  };

  const deletePersonRelation = (index: number) => {
    const { relations } = form;
    relations.splice(index, 1);
    // eslint-disable-next-line
    for (let i = 0; i < relations.length; i++) {
      relations[i].index = i;
    }
  };

  // 提交按钮
  const handleSubmit = async () => {
    const res = await formRef.value?.validate();
    setLoading(true);
    try {
      if (personIdNumber) {
        await updatePersonApi(personIdNumber, form);
        Message.success(t('submit.update.success'));
        setLoading(false);
        router.push({
          name: 'DataPersonDetail',
          query: { personId: personIdNumber },
        });
      } else {
        await createPersonApi(form);
        Message.success(t('submit.create.success'));
        setLoading(false);
        router.push({
          name: 'DataPerson',
        });
      }
    } catch (error) {
      // console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (personIdNumber) {
      router.push({
        name: 'DataPersonDetail',
        query: { personId: personIdNumber },
      });
    } else {
      router.push({
        name: 'DataPerson',
      });
    }
  };
  
  const fileList = ref<FileItem[]>([]);


  const customRequest = (option: RequestOption): UploadRequest => {
    const { onProgress, onError, onSuccess, fileItem } = option;
    const xhr = new XMLHttpRequest();
    if (xhr.upload) {
      xhr.upload.onprogress = function (event) {
        let percent = 0;
        if (event.total > 0) {
          percent = event.loaded / event.total;
        }
        onProgress(percent, event);
      };
    }
    xhr.onerror = function error(e) {
      onError(e);
    };
    xhr.onload = function onload() {
      if (xhr.status < 200 || xhr.status >= 300) {
        Message.error(t('上传失败'));
        return onError(xhr.responseText);
      }

      Message.success(t('上传成功'));
      const response = JSON.parse(xhr.response);
      const { id, uid, name, obj_name, url } = response.data;
      form.attachments.push({
        id, uid, name, obj_name, url
      })
      return onSuccess(xhr.response);
    };
    const formData = new FormData();
    formData.append('file', fileItem.file as Blob);
    const token = getToken();
    let url = '/api/v1/data/attachement/upload';
    if (import.meta.env.VITE_API_BASE_URL) {
      url = `${import.meta.env.VITE_API_BASE_URL}/api/v1/data/attachement/upload`;
    }
    xhr.open('post', url, true);
    xhr.setRequestHeader('Authorization', `Bearer ${token}`);
    xhr.send(formData);

    return {
      abort() {
        xhr.abort();
      },
    };
  };

  const onBeforeRemove = (file: FileItem): Promise<boolean> => {
    return new Promise((resolve) => {
      const index = form.attachments.findIndex((item) => item.id === file.uid);
      if (index > -1) {
        form.attachments.splice(index, 1);
      }
      resolve(true);
    });
  };
</script>
