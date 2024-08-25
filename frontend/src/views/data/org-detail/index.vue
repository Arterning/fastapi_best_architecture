<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :routes="routes" />
      <a-card :title="$t('组织详情')" class="general-card">
        <div class="content">
          <a-tabs default-active-key="1">
            <a-tab-pane key="1" title="基础信息">
              <a-card :loading="loading" class="info-card">
                <template #title>
                  <BaseInfo class="icon" />
                  {{ $t('基础信息') }}
                </template>
                <a-descriptions :data="showData" :column="1"></a-descriptions>
              </a-card>
            </a-tab-pane>

            <a-tab-pane key="2" title="关联文件">
              <a-space style="padding-top: 22px" />
              <a-row :gutter="20">
                <a-col>
                  <a-list
                    :data="detailInfo.docs"
                    :max-height="800"
                    :loading="loading"
                  >
                    <template #header>
                      <word class="icon" /> 关联文件
                    </template>
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
              </a-row>
            </a-tab-pane>

            <a-tab-pane key="3" title="关联人物">
              <a-col>
                <a-list
                  :data="detailInfo.persons"
                  :max-height="800"
                  :loading="loading"
                >
                  <template #header> <user class="icon" /> 关联人物 </template>
                  <template #item="{ item, index }">
                    <a-list-item
                      :key="index"
                      class="ResultItem"
                      @click="
                        $router.push({
                          name: 'DataPersonDetail',
                          query: { personId: item.id },
                        })
                      "
                    >
                      {{ item.name }}
                    </a-list-item>
                  </template>
                </a-list>
              </a-col>
            </a-tab-pane>

            <a-tab-pane key="4" title="部门架构">
              <a-space style="padding-top: 22px" />
              <a-row :gutter="20">
                <a-col :span="12">
                  <a-card :loading="loading">
                    <template #title>
                      {{ $t('上级部门') }}
                    </template>
                    <a-link
                      v-if="detailInfo.parent != null"
                      @click="
                        $router.push({
                          name: 'DataOrgDetail',
                          query: { orgId: detailInfo.parent.id },
                        })
                      "
                      >{{ detailInfo.parent.name }}
                    </a-link>
                    <template v-else>
                      <a-empty />
                    </template>
                  </a-card>
                </a-col>
                <a-col :span="12">
                  <a-list
                    :data="detailInfo.children"
                    :max-height="240"
                    :loading="loading"
                  >
                    <template #header>
                      {{ $t('下级部门') }}
                    </template>
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
              </a-row>

              <a-space style="padding-top: 22px" />
              <a-card class="info-card">
                <template #title>
                  {{ $t('组织成员架构图') }}
                </template>
                <OrgTree v-if="!loading" :treeData="treeData" />
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
  import OrgTree from '@/components/org-tree/index.vue';
  import Footer from '@/components/footer/index.vue';
  import Breadcrumb from '@/components/link-breadcrumb/index.vue';
  import useLoading from '@/hooks/loading';
  import { useRoute } from 'vue-router';
  import { queryOrgDetail } from '@/api/org';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  const detailInfo = ref<Record<string, any>>({});
  const treeData = ref<Record<string, any>>({});
  const showData = computed<DescData[]>(() => [
    {
      label: t('组织名'),
      value: detailInfo.value?.name,
    },
    {
      label: t('详细信息'),
      value: detailInfo.value?.detail,
    },
  ]);

  // 请求数据
  const fetchData = async (orgId: number) => {
    setLoading(true);
    try {
      const res = await queryOrgDetail(orgId);
      detailInfo.value = res;
      const { parent } = detailInfo.value;
      const { children } = detailInfo.value;
      const orgChildren = [];
      if (children) {
        orgChildren.push({
          id: 'subOrgs',
          pid: detailInfo.value.id,
          label: t('下级部门'),
          style: { color: '#fff', background: '#108ffe' },
          children: children.map((item: Record<string, any>) => {
            return {
              id: item.id,
              pid: 'subOrgs',
              label: item.name,
            };
          }),
        });
      }

      const { persons } = detailInfo.value;
      if (persons) {
        orgChildren.push({
          id: 'persons',
          pid: detailInfo.value.id,
          label: t('成员'),
          style: { color: '#fff', background: '#108ffe' },
          children: persons.map((item: Record<string, any>) => {
            return {
              id: item.id,
              pid: 'persons',
              label: item.name,
            };
          }),
        });
      }

      if (parent) {
        treeData.value = {
          id: parent.id,
          label: parent.name,
          style: { color: '#fff', background: '#108ffe' },
          children: [
            {
              id: detailInfo.value.id,
              pid: parent.id,
              label: detailInfo.value.name,
              style: { color: '#fff', background: '#108ffe' },
              children: orgChildren,
            },
          ],
        };
      } else {
        treeData.value = {
          id: detailInfo.value.id,
          label: detailInfo.value.name,
          style: { color: '#fff', background: '#108ffe' },
          children: orgChildren,
        };
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const route = useRoute();
  const { orgId } = route.query;
  const orgIdNumber = Number(orgId);
  if (orgIdNumber) {
    fetchData(orgIdNumber);
  }

  const routes = [
    {
      path: '/data/org',
      label: '机构管理',
    },
    {
      path: `/data/org-detail?orgId=${orgId}`,
      label: '组织详情',
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
