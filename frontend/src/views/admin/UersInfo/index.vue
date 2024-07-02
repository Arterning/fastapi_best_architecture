<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.system'), $t('menu.system.sysInfo')]" />
      <a-card :title="$t('menu.system.sysInfo')" class="general-card">
        <a-row>
          <a-col :flex="1"> </a-col>
          <a-col :flex="4">
            <a-avatar :style="{ backgroundColor: '#14C9C9' }" :size="120">
              <IconUser />
              <template #trigger-icon>
                <IconEdit />
              </template>
            </a-avatar>
          </a-col>
          <a-col :flex="20" class="information">
            <a-row class="lis">
              <a-col :span="12"
                ><icon-user /> 用 户 名: {{ userinfo?.username }}</a-col
              >
              <a-col
                :span="12"
                @mouseenter="showEditor"
                @mouseleave="hideEditor"
                ><icon-idcard /> 用户昵称: {{ userinfo?.nickname }}
                <icon-edit v-if="Visible" @click="inputEditor" />
              </a-col>
            </a-row>
            <a-row class="lis">
              <a-col
                :span="12"
                @mouseenter="showEditor"
                @mouseleave="hideEditor"
              >
                <icon-email /> 用户邮箱: {{ userinfo?.email }}
                <icon-edit v-if="Visible" @click="inputEditor"
              /></a-col>
              <a-col
                :span="12"
                @mouseenter="showEditor"
                @mouseleave="hideEditor"
              >
                <icon-phone /> 用户电话: {{ userinfo?.phone }}
                <icon-edit v-if="Visible" @click="inputEditor"
              /></a-col>
            </a-row>
            <a-row class="lis">
              <a-col :span="12">
                <icon-schedule />
                加入时间: {{ userinfo?.join_time }}</a-col
              >
              <a-col :span="12">
                <icon-schedule /> 登录时间:
                {{ userinfo?.last_login_time }}</a-col
              >
            </a-row>
          </a-col>
        </a-row>
        <a-divider />

        <div class="content-modal"> </div>
      </a-card>
    </a-layout>
  </div>
  <div class="footer">
    <Footer />
  </div>
</template>

<script lang="ts" setup>
  import Breadcrumb from '@/components/breadcrumb/index.vue';
  import Footer from '@/components/footer/index.vue';
  import { getUserInfo } from '@/api/user';
  import { ref, onMounted } from 'vue';

  const userinfo = ref<any>(null);
  const Visible = ref(false);

  const fetchUserInfo = async () => {
    try {
      const results = await getUserInfo();
      userinfo.value = results;
      console.log(userinfo.value);
    } catch (error) {
      console.error('搜索失败:', error);
    }
  };
  onMounted(fetchUserInfo);
  const showEditor = () => {
    // Visible.value = true;
  };

  const hideEditor = () => {
    // Visible.value = false;
  };

  const inputEditor = () => {};
</script>

<style lang="less" scoped>
  .information {
    font-size: 16px;
  }
  .lis {
    margin: 10px 0;
  }
  // .editor:hover::after {
  //   content: '<icon-edit />';
  // }
</style>
