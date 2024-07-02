<template>
  <div style="border: 1px solid #ccc">
    <Toolbar
      style="border-bottom: 1px solid #ccc;"
      :editor="editorRef"
      :defaultConfig="toolbarConfig"
      :mode="mode"
    />
    <Editor
      style="height: 500px; overflow-y: hidden;"
      v-model="valueHtml"
      :defaultConfig="editorConfig"
      :mode="mode"
      @onCreated="handleCreated"
    />
  </div>
</template>

<script lang="ts" setup>
import '@wangeditor/editor/dist/css/style.css'; // 引入 css

import { ref, shallowRef, watch, defineProps, defineEmits, onBeforeUnmount } from 'vue';
import { Editor, Toolbar } from '@wangeditor/editor-for-vue';
import type { IDomEditor } from '@wangeditor/editor'; // 导入 Editor 类型

// 接收父组件内容
interface PropsType {
  modelValue?: string;
  mode?: string;
}

const props = defineProps<PropsType>();
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef<IDomEditor | undefined>(undefined);
const valueHtml = ref<string | undefined>(props.modelValue);

// 监听 props.modelValue 的变化
watch(() => props.modelValue, (newValue) => {
  valueHtml.value = newValue;
});

// 监听 valueHtml 的变化并通知父组件
watch(valueHtml, (newHtml) => {
  if (newHtml !== props.modelValue) {
    emit('update:modelValue', newHtml || '');
  }
});

// 配置信息
const toolbarConfig = {};
const editorConfig = { placeholder: '请输入内容...' };

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  if (editorRef.value !== undefined) {
    editorRef.value.destroy();
  }
});

const handleCreated = (editor: IDomEditor) => {
  editorRef.value = editor; // 记录 editor 实例，重要！
};
</script>

<style lang="less" scoped>

</style>
