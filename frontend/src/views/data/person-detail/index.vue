<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card class="general-card">
        <template #title>
          <a-space size="large">
            人物详情
            <a-link @click="handleEdit">
              <template #icon> <icon-edit /> </template>编辑人物</a-link
            >
          </a-space>
        </template>
        <div class="content">
          <a-tabs default-active-key="1">
            <a-tab-pane key="1" title="基础信息">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <BaseInfo class="icon" />
                  {{ $t('人物照片') }}
                </template>
                <a-image-preview-group infinite>
                  <a-space>
                    <a-image
                      v-for="a in detailInfo.attachments"
                      :key="a.id"
                      :src="getPreviewURL(a.obj_name)"
                    />
                  </a-space>
                </a-image-preview-group>
              </a-card>
              <a-space style="padding-top: 22px" />
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <BaseInfo class="icon" />
                  {{ $t('基础信息') }}
                </template>
                <a-descriptions :data="showData" :column="1"></a-descriptions>
              </a-card>
              <a-space style="padding-top: 22px" />
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <user class="icon" />
                  {{ $t('人物简历') }}
                </template>
                <p v-if="detailInfo.detail !== null">{{ detailInfo.detail }}</p>
                <a-empty v-else />
              </a-card>
              <a-space style="padding-top: 22px" />
            </a-tab-pane>

            <a-tab-pane key="2" title="关联文件">
              <a-col>
                <a-list
                  :data="detailInfo.docs"
                  :loading="loading"
                  :hoverable="true"
                  :max-height="800"
                >
                  <template #header> <word class="icon" /> 关联文件 </template>
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
            </a-tab-pane>

            <a-tab-pane key="3" title="关联组织">
              <a-col>
                <a-list
                  :data="detailInfo.orgs"
                  :loading="loading"
                  :hoverable="true"
                  :max-height="800"
                >
                  <template #header> <organ class="icon" /> 关联组织 </template>
                  <template #item="{ item, index }">
                    <a-list-item
                      :key="index"
                      class="ResultItem"
                      @click="
                        $router.push({
                          name: 'DataOrgDetail',
                          query: { orgId: item.id },
                        })
                      "
                    >
                      {{ item.name }}
                    </a-list-item>
                  </template>
                </a-list>
              </a-col>
            </a-tab-pane>

            <a-tab-pane key="4" title="人物关系图">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <PersonRelation class="icon" />
                  {{ $t('人物关系') }}
                </template>
                <Relation :data="detailInfo.relation_json" />
              </a-card>
            </a-tab-pane>

            <a-tab-pane key="5" title="人物动态">
              <a-card class="info-card">
                <template #title>
                  {{ $t('人物动态') }}
                </template>
                <a-timeline>
                  <a-timeline-item
                    v-for="(opion, index) in detailInfo.activity"
                    :label="opion.datetime"
                    :key="index"
                    >{{ opion.content }}</a-timeline-item
                  >
                </a-timeline>
              </a-card>
            </a-tab-pane>
          </a-tabs>
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
  import Relation from '@/components/relation/index.vue';
  import useLoading from '@/hooks/loading';
  import { useRoute } from 'vue-router';
  import { queryPersonDetail } from '@/api/person';
  import router from '@/router';
  import { getPreviewURL } from '@/utils/image';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  const detailInfo = ref<Record<string, any>>({});
  const showData = computed<DescData[]>(() => [
    {
      label: t('人物名'),
      value: detailInfo.value?.name,
    },
  ]);

  // 请求数据
  const fetchData = async (personId: number) => {
    setLoading(true);
    try {
      const res = await queryPersonDetail(personId);
      console.log(res);
      
      detailInfo.value = res;
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const route = useRoute();
  const { personId } = route.query;
  const personIdNumber = Number(personId);
  if (personIdNumber) {
    fetchData(personIdNumber);
  }

  const routes = [
    {
      path: '/data/person',
      label: '人物管理',
    },
    {
      path: `/data/person-detail?personId=${personId}`,
      label: '人物详情',
    },
  ];

  const handleEdit = () => {
    router.push({
      name: 'DataPersonEdit',
      query: { personId: detailInfo.value.id },
    });
  };

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
