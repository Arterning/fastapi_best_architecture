<template>
  <a-spin :spinning="state.loading" tip="加载中...">
    <div class="pdf-preview">
      <div class="pdf-wrap">
        <vue-pdf-embed
          :page="state.pageNum"
          :source="state.source"
          :style="scale"
          class="vue-pdf-embed"
        />
      </div>
      <div class="page-tool">
        <div class="page-tool-item" @click="lastPage">上一页</div>
        <div class="page-tool-item" @click="nextPage">下一页</div>
        <div class="page-tool-item">
          {{ state.pageNum }}/{{ state.numPages }}
        </div>
        <div class="page-tool-item" @click="pageZoomOut">放大</div>
        <div class="page-tool-item" @click="pageZoomIn">缩小</div>
        <!-- <div class="page-tool-item" @click="downloadPDF">下载</div> -->
      </div>
    </div>
  </a-spin>
</template>
<script lang="ts" setup>
  import VuePdfEmbed from 'vue-pdf-embed';
  import { createLoadingTask } from 'vue3-pdfjs';

  import { reactive, onMounted, computed } from 'vue';

  const props = defineProps({
    pdfUrl: {
      type: String,
      required: true,
    },
  });

  const state = reactive({
    source: props.pdfUrl,
    pageNum: 1,
    scale: 1,
    numPages: 0,
    loading: true,
  });
  
  // 下载pdf
  // function downloadPDF() {
  //   fetch(encodeURI(props.pdfUrl)).then((res) => {
  //     res.blob().then((myBlob) => {
  //       const href = URL.createObjectURL(myBlob);
  //       const a = document.createElement('a');
  //       a.href = href;
  //       a.download = 'report.pdf'; // 下载文件重命名，并指定文件扩展名为 ".pdf"
  //       document.body.appendChild(a); // 将<a>元素添加到文档中，以便进行点击下载
  //       a.click();
  //       document.body.removeChild(a); // 下载完成后移除<a>元素
  //     });
  //   });
  // }

  onMounted(() => {
    const loadingTask = createLoadingTask(state.source);
    state.loading = true; // 添加一个loading状态
    loadingTask.promise.then((pdf: { numPages: number }) => {
      state.numPages = pdf.numPages;
      state.loading = false; // 加载完成后将loading状态设置为false
    });
  });

  const scale = computed(() => `transform:scale(${state.scale})`);

  function lastPage() {
    if (state.pageNum > 1) {
      state.pageNum -= 1;
    }
  }

  function nextPage() {
    if (state.pageNum < state.numPages) {
      state.pageNum += 1;
    }
  }

  function pageZoomOut() {
    if (state.scale < 2) {
      state.scale += 0.1;
    }
  }

  function pageZoomIn() {
    if (state.scale > 1) {
      state.scale -= 0.1;
    }
  }
</script>
<style lang="css" scoped>
  .pdf-preview {
    position: relative;
    height: 100%;
    padding: 20px 0;
    box-sizing: border-box;
    background-color: #e9e9e9;
  }

  .pdf-wrap {
    overflow-y: auto;
  }

  .vue-pdf-embed {
    text-align: center;
    width: 815px;
    height: 815px;
    border: 1px solid #e5e5e5;
    margin: 0 auto;
    box-sizing: border-box;
  }

  .page-tool {
    position: absolute;
    bottom: 35px;
    padding-left: 15px;
    padding-right: 15px;
    display: flex;
    align-items: center;
    background: rgb(66, 66, 66);
    color: white;
    border-radius: 19px;
    z-index: 100;
    cursor: pointer;
    margin-left: 50%;
    transform: translateX(-50%);
  }

  .page-tool-item {
    padding: 8px 15px;
    padding-left: 10px;
    cursor: pointer;
  }
</style>
