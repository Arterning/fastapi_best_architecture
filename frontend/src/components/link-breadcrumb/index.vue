<template>
  <a-breadcrumb class="container-breadcrumb">
    <a-breadcrumb-item>
      <icon-apps />
    </a-breadcrumb-item>
    <a-breadcrumb-item v-for="r in routes" :key="r.label">
      <a-link :href="r.path">{{ $t(r.label) }}</a-link>
    </a-breadcrumb-item>
  </a-breadcrumb>
</template>

<script lang="ts" setup>
  import { PropType } from 'vue';

  interface RouteItem {
    label: string;
    path: string;
  }

  defineProps({
    routes: {
      type: Array as PropType<RouteItem[]>,
      default() {
        return [];
      },
    },
  });
</script>

<style lang="less" scoped>
  .container-breadcrumb {
    margin: 16px 0;

    :deep(.arco-breadcrumb-item) {
      color: rgb(var(--gray-6));

      &:last-child {
        color: rgb(var(--gray-8));
      }
    }
  }
</style>
