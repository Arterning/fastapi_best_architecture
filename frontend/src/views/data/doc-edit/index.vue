<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card :title="$t('编辑文件')" class="general-card">
        <a-space direction="vertical" size="large" :style="{ width: '80%' }">
          <a-form ref="formRef" :model="form">
            <a-form-item
              :feedback="true"
              :label="$t('标题')"
              :rules="[{ required: true, message: $t('title') }]"
              field="title"
            >
              <a-input v-model="form.title" :placeholder="$t('标题')"></a-input>
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
                  添加标签
                </a-tag>
              </a-space>
            </a-form-item>
            <a-form-item :label="$t('人物')" field="persons">
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

            <a-form-item :label="$t('组织')" field="orgs">
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

            <a-form-item field="content">
              <a-textarea
                v-model="form.content"
                style="overflow: scroll; height: 500px"
                :placeholder="$t('文件内容')"
              ></a-textarea>
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
  import { useI18n } from 'vue-i18n';
  import { computed, reactive, ref, nextTick, onMounted } from 'vue';
  import {
    createDocApi,
    queryDocDetail,
    DocReq,
    updateDocApi,
  } from '@/api/doc';
  import { PersonRes, queryPersonAll, queryPersonList } from '@/api/person';
  import { OrgRes, queryOrgAll, queryOrgList } from '@/api/org';
  // 导入编辑器
  import { useRoute, useRouter } from 'vue-router';
  import Breadcrumb from '@/components/link-breadcrumb/index.vue';
  import useLoading from '@/hooks/loading';
  import { Message } from '@arco-design/web-vue';
  import router from '@/router';

  const { t } = useI18n();
  const formRef = ref();
  const { loading, setLoading } = useLoading(false);

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

  const tags = ref<string[]>([]);
  const inputRef = ref<HTMLInputElement>();
  const showInput = ref(false);
  const inputVal = ref('');

  // 请求数据
  const fetchData = async (docId: number) => {
    setLoading(true);
    try {
      const res = await queryDocDetail(docId);
      resetForm(res);

      if (res?.persons) {
        persons.value = [...res.persons];
      }

      if (res?.orgs) {
        orgs.value = [...res.orgs];
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

      form.persons = data.persons?.map((item: Record<any, any>) => item.id);
      form.orgs = data.orgs?.map((item: Record<any, any>) => item.id);
      form.tags = data.tags?.map((item: Record<any, any>) => item.name);

      if (form.tags) {
        tags.value = [...form.tags];
      }
    });
  };

  const route = useRoute();
  const { docId } = route.query;
  const docIdNumber = Number(docId);
  if (docIdNumber) {
    fetchData(docIdNumber);
  }

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

  const handleRemove = (key: string) => {
    tags.value = tags.value.filter((tag) => tag !== key);
    form.tags = form.tags?.filter((tag) => tag !== key);
  };

  const handleAdd = () => {
    if (inputVal.value) {
      tags.value.push(inputVal.value);
      form.tags?.push(inputVal.value);
      inputVal.value = '';
    }
    showInput.value = false;
  };

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

  const handleEdit = () => {
    showInput.value = true;

    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus();
      }
    });
  };

  const routes = [
    {
      path: '/data/doc',
      label: '文件管理',
    },
    {
      path: `/data/doc-edit?docId=${docIdNumber}`,
      label: '编辑文件',
    },
  ];

  // 提交按钮
  const handleSubmit = async () => {
    const res = await formRef.value?.validate();
    setLoading(true);
    try {
      if (docIdNumber) {
        await updateDocApi(docIdNumber, form);
        Message.success(t('submit.update.success'));
        setLoading(false);
        router.push({
          name: 'DataDocDetail',
          query: { docId: docIdNumber },
        });
      } else {
        await createDocApi(form);
        Message.success(t('submit.create.success'));
        setLoading(false);
        router.push({
          name: 'DataDoc',
        });
      }
    } catch (error) {
      // console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (docIdNumber) {
      router.push({
        name: 'DataDocDetail',
        query: { docId: docIdNumber },
      });
    } else {
      router.push({
        name: 'DataDoc',
      });
    }
  };
</script>
