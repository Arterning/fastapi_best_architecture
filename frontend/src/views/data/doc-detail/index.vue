<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card class="general-card">
        <template #title>
          <a-space size="large">
            文件详情
            <a-link @click="handleEdit">
              <template #icon> <icon-edit /> </template>编辑文件</a-link
            >
            <a-link v-if="detailInfo?.uuid" @click="handleClick">
              <template #icon> <icon-file-pdf /> </template>阅读原文</a-link
            >
            <a-link @click="FollowFile(detailInfo.id)">
              <template #icon> <icon-star /></template> 收藏
            </a-link>
          </a-space>
        </template>
        <div class="content">
          <a-tabs default-active-key="1">
            <a-tab-pane key="1" title="基础信息">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <BaseInfo class="icon" />
                  {{ $t('基础信息') }}
                </template>
                <a-descriptions :data="showData" :column="1"> </a-descriptions>
              </a-card>
              <a-space style="padding-top: 22px" />
              <a-card :loading="loading || ocrLoading" class="info-card">
                <template #title>
                  {{ $t('内容') }}
                </template>
                <a-button @click="extractOCR" style="margin-bottom: 20px;">重新提取</a-button>
                <a-scrollbar style="height:500px;overflow: auto;">
                  <pre style="font-size: large;"> {{ detailInfo.content }}</pre>
                </a-scrollbar>
              </a-card>
            </a-tab-pane>

            <a-tab-pane key="2" title="文件标签">
              <a-space style="padding-top: 22px" />
              <a-row :gutter="20">
                <a-col :span="24">
                  <a-card :loading="loading" class="info-card">
                    <template #title>
                      {{ $t('标签') }}
                    </template>
                    <a-space wrap>
                      <a-tag v-for="tag of detailInfo.tags" :key="tag.id">
                        {{ tag.name }}
                      </a-tag>
                    </a-space>
                  </a-card>
                </a-col>
              </a-row>
            </a-tab-pane>
          </a-tabs>

          <a-modal
            v-model:visible="visible"
            @ok="handleOk"
            @cancel="handleCancel"
            :fullscreen="true"
            :bodyStyle="{ height: '100%' }"
          >
            <template #title> {{ detailInfo?.title }} </template>
            <iframe
              id="viewer"
              width="100%"
              height="100%"
              v-if="visible && detailInfo?.uuid"
              :src="getPreviewURL(detailInfo?.uuid)"
            />
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
  import { computed, ref } from 'vue';
  import { DescData, Message } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import Footer from '@/components/footer/index.vue';
  import Breadcrumb from '@/components/link-breadcrumb/index.vue';
  import useLoading from '@/hooks/loading';
  import { useRoute } from 'vue-router';
  import { followDocApi, queryDocDetail } from '@/api/doc';
  import { ocrDoc } from '@/api/ocr';
  import router from '@/router';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);
  const { loading: ocrLoading, setLoading: setOCRLoading} = useLoading(false);

  const visible = ref(false);

  const handleClick = () => {
    visible.value = true;
    // let url = `/api/v1/data/docs/preview/${detailInfo.value.uuid}#toolbar=0`;
    // if (import.meta.env.VITE_API_BASE_URL) {
    //     url = `${import.meta.env.VITE_API_BASE_URL}/api/v1/data/docs/preview/${detailInfo.value.uuid}#toolbar=0`;
    // }
    // window.open(url);
  };

  const handleEdit = () => {
    router.push({
      name: 'DataDocEdit',
      query: { docId: detailInfo.value.id },
    });
  };

  const handleOk = () => {
    visible.value = false;
  };
  const handleCancel = () => {
    visible.value = false;
  };

  const detailInfo = ref<Record<string, any>>({});
  const showData = computed<DescData[]>(() => [
    {
      label: t('文件名'),
      value: detailInfo.value?.title,
    },
  ]);

  // 请求数据
  const fetchData = async (docId: number) => {
    setLoading(true);
    try {
      const res = await queryDocDetail(docId);
      detailInfo.value = res;
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const route = useRoute();
  const { docId } = route.query;
  const docIdNumber = Number(docId);
  if (docIdNumber) {
    fetchData(docIdNumber);
  }

  const getPreviewURL = (uid: string) => {
    const { origin } = window.location;
    const BASE = import.meta.env.VITE_API_BASE_URL;
    // 判断用户是否是admin 如果不是，则需要在URL后面加上#toolbar=0
    if (BASE) {
      return `${BASE}/api/v1/data/docs/preview/${uid}`;
    }
    return `${origin}/api/v1/data/docs/preview/${uid}`;
  };

  const routes = [
    {
      path: '/data/doc',
      label: '文件管理',
    },
    {
      path: `/data/doc-detail?docId=${docId}`,
      label: '数据详情',
    },
  ];

  

  const FollowFile = async (id: number) => {
    await followDocApi(id);
    Message.success(t('submit.operate.success'));
  };


  const extractOCR = async () => {
    setOCRLoading(true)
    try {
      const response =  await ocrDoc(detailInfo.value.id)
      detailInfo.value.content = response.content
      Message.success(t('submit.operate.success'));
    } catch (err) {
      console.error(err)
    } finally {
      setOCRLoading(false)
    }
  }
</script>

<style lang="less" scoped>
  .info-card {
    border-radius: 20px;
    border-bottom-width: 2px;

    & > .arco-card-header {
      height: auto;
      padding: 20px;
      border: none;
    }

    & > .arco-card-body {
      padding: 0 20px 20px 20px;
    }
  }
  .icon {
    width: 20px;
    height: 20px;
    margin-bottom: -3px;
  }
</style>
