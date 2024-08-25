<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card :title="$t('议题详情')" class="general-card">
        <div class="content">
          <a-card :loading="loading" class="info-card">
            <template #title>
              {{ $t('基础信息') }}
            </template>
            <a-descriptions :data="showData" :column="1"></a-descriptions>
          </a-card>
          <a-space style="padding-top: 22px" />
          <a-col>
            <a-list
              :data="detailInfo.docs"
              :max-height="240"
              :loading="loading"
            >
              <template #header> <word class="icon" /> 议题文件 </template>
              <template #item="{ item, index }">
                <a-list-item
                  :key="index"
                  class="ResultItem"
                  @click="
                    $router.push({
                      name: 'DataDocDetail',
                      query: { docId: item.id },
                    })
                  "
                >
                  {{ item.title }}
                </a-list-item>
              </template>
            </a-list>
          </a-col>
          <a-space style="padding-top: 22px" />
          <a-card :loading="loading" class="info-card">
            <template #title>
              {{ $t('议题脉络') }}
            </template>
            <a-timeline direction="vertical" pending>
              <a-timeline-item
                v-for="(item, index) in detailInfo.his"
                :key="index"
              >
                <a-row
                  :style="{ display: 'inline-flex', alignItems: 'center' }"
                >
                  <div :style="{ marginBottom: '6px'}">
                    {{ item.title }}
                    <div>
                      {{ item.detail }}
                    </div>
                  </div>
                </a-row>
              </a-timeline-item>
            </a-timeline>
          </a-card>

          <a-space style="padding-top: 22px" />
          <a-row :gutter="20">
            <a-col :span="12">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <user class="icon" />
                  {{ $t('关联人物') }}
                </template>
                <a-list :data="detailInfo.persons" :max-height="240">
                  <template #item="{ item, index }">
                    <a-list-item :key="index">
                      <a-link
                        @click="
                          $router.push({
                            name: 'DataPersonDetail',
                            query: { personId: item.id },
                          })
                        "
                        >{{ item.name }}</a-link
                      >
                    </a-list-item>
                  </template>
                </a-list>
              </a-card>
            </a-col>
            <a-col :span="12">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <organ class="icon" />
                  {{ $t('关联组织') }}
                </template>
                <a-list :data="detailInfo.orgs" :max-height="240">
                  <template #item="{ item, index }">
                    <a-list-item :key="index">
                      <a-link
                        @click="
                          $router.push({
                            name: 'DataOrgDetail',
                            query: { orgId: item.id },
                          })
                        "
                        >{{ item.name }}</a-link
                      >
                    </a-list-item>
                  </template>
                </a-list>
              </a-card>
            </a-col>
          </a-row>
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
  import { querySubjectDetail } from '@/api/subject';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  const detailInfo = ref<Record<string, any>>({});
  const showData = computed<DescData[]>(() => [
    {
      label: t('议题名'),
      value: detailInfo.value?.name,
    },
    {
      label: t('议题类型'),
      value: detailInfo.value?.type,
    },
    {
      label: t('详细信息'),
      value: detailInfo.value?.detail,
    },
  ]);

  // 请求数据
  const fetchData = async (subjectId: number) => {
    setLoading(true);
    try {
      const res = await querySubjectDetail(subjectId);
      detailInfo.value = res;
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const route = useRoute();
  const { subjectId } = route.query;
  const subjectIdNumber = Number(subjectId);
  if (subjectIdNumber) {
    fetchData(subjectIdNumber);
  }

  const routes = [
    {
      path: '/data/subject',
      label: '事件数据',
    },
    {
      path: `/data/subject-detail?subject=${subjectId}`,
      label: '事件详情',
    },
  ];

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
  .ResultItem:hover {
    // background-color: #f0f0f0;
    opacity: 1.5;
    cursor: pointer;
    color: rgb(22, 93, 255);
  }

  .icon {
    width: 20px;
    height: 20px;
    margin-bottom: -3px;
  }
</style>
