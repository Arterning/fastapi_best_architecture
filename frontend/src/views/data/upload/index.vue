<template>
  <div class="container">
    <a-layout style="padding: 0 18px">
      <Breadcrumb :items="[$t('menu.data'), $t('menu.upload')]" />
      <a-card :title="$t('menu.upload')" class="general-card">
        <a-card :style="{ width: '100%', marginBottom: '20px' }" title="上传选项">
          <a-space size="large">
            <a-checkbox v-model="uploadDirectory" :default-checked="false"
            >上传目录</a-checkbox
            >
          </a-space
          >
        </a-card>
        <a-upload
            draggable
            :directory="uploadDirectory"
            :custom-request="customRequest"
            accept="application/pdf,application/zip"
        />
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
    UploadRequest,
    Modal,
  } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import { computed, reactive, ref, nextTick, onMounted } from 'vue';
  import Footer from '@/components/footer/index.vue';
  import { getToken } from '@/utils/auth';

  const { t } = useI18n();

  const trans = ref(true);
  const digest = ref(true);
  const person = ref(true);
  const uploadDirectory = ref(false);
  

  const beforeUpload = (file: File): Promise<boolean> => {
    if (uploadDirectory.value) {
      return Promise.resolve(true);
    }
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
        Message.error(t('导入失败'));
        return onError(xhr.responseText);
      }

      Message.success(t('导入成功'));
      return onSuccess(xhr.response);
    };
    const formData = new FormData();
    formData.append('file', fileItem.file as Blob);
    const token = getToken();
    let url = '/api/v1/data/docs/upload';
    if (import.meta.env.VITE_API_BASE_URL) {
      url = `${import.meta.env.VITE_API_BASE_URL}/api/v1/data/docs/upload`;
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
</script>
