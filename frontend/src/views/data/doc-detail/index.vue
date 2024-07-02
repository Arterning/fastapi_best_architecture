<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card :title="$t('文件详情')" class="general-card">
        <div class="content">
          <a-card :title="$t('基础信息')" :loading="loading" class="info-card">
            <a-descriptions :data="showData" :column="1"> </a-descriptions>
          </a-card>

          <a-space style="padding-top: 22px" />
          <a-row :gutter="20">
            <a-col :span="24">
              <a-card :title="$t('标签')" :loading="loading" class="info-card">
                <a-space wrap>
                  <a-tag v-for="tag of detailInfo.tags" :key="tag.id">
                    {{ tag.name }}
                  </a-tag>
                </a-space>
              </a-card>
            </a-col>
          </a-row>

          <a-space style="padding-top: 22px" />

          <a-modal
            v-model:visible="visible"
            width="auto"
            @ok="handleOk"
            @cancel="handleCancel"
          >
            <template #title> 预览文件 </template>
            <Preview
              v-if="visible && detailInfo?.uuid"
              :pdfUrl="getPreviewURL(detailInfo?.uuid)"
            />
          </a-modal>

          <a-space style="padding-top: 22px" />
          <a-card :title="$t('内容')" :loading="loading" class="info-card">
            <a-typography>
              <a-typography-paragraph>
                <a-link v-if="detailInfo?.uuid" @click="handleClick"
                  >原文地址</a-link
                >
              </a-typography-paragraph>
            </a-typography>
            <div v-html="detailInfo.content.replaceAll('\n', '<br>')"></div>
          </a-card>
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
  import { DescData } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import Footer from '@/components/footer/index.vue';
  import Breadcrumb from '@/components/link-breadcrumb/index.vue';
  import useLoading from '@/hooks/loading';
  import { useRoute } from 'vue-router';
  import { queryDocDetail } from '@/api/doc';
  import Preview from '@/components/preview/index.vue';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  const visible = ref(false);

  const handleClick = () => {
    visible.value = true;
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
    {
      label: t('时间'),
      value: detailInfo.value?.time,
    },
    {
      label: t('地点'),
      value: detailInfo.value?.location,
    },
    {
      label: t('主题'),
      value: detailInfo.value?.subject,
    },
    {
      label: t('来源'),
      value: detailInfo.value?.source,
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
    const BASE = import.meta.env.VITE_API_BASE_URL
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
</script>

<style lang="less">
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
</style>
