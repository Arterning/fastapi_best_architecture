<template>
  <a-button
    :shape="'circle'"
    class="nav-btn"
    type="outline"
    @click="handleClick"
  >
    <template #icon>
      <icon-search />
    </template>
  </a-button>
  <a-modal v-model:visible="visible" @ok="handleOk" @cancel="handleCancel">
    <template #title>
      <a-space direction="vertical" size="large" class="modal-title">
        <a-input
          v-model="searchQuery"
          class="search"
          placeholder="Search"
          allow-clear
          @input="handleInput"
          @keyup.enter="handleEnter"
        >
          <template #prefix>
            <icon-search />
          </template>
        </a-input>
      </a-space>
    </template>
    <div v-if="!searchQuery" v-show="showHistory" class="history">
      <div class="history-header">
        <div>最近搜索</div>
        <span class="del" @click="clearHistory">清除全部</span>
      </div>
      <a-list>
        <a-list-item
          v-for="(item, index) in historyItems"
          :key="item"
          class="history-item"
          @click="historyHandle(item)"
        >
          <icon-history />
          <span class="time">{{ item }}</span>
          <icon-delete
            type="close"
            class="delete-icon"
            @click="deleteHistoryItem(index)"
          />
        </a-list-item>
      </a-list>
    </div>
    <div v-else class="searchResults">
      <div>搜索到{{ filteredResults.length }}个结果</div>

      <a-list :max-height="240">
        <!-- <a :href="result.url"> </a> -->
        <!-- <router-link :to=""> -->

        <a-list-item
          v-for="result in filteredResults"
          :key="result.id"
          class="ResultItem"
          @click="handleResultClick(result.id)"
        >
          {{ result.title }}
        </a-list-item>

        <!-- </router-link> -->
      </a-list>
    </div>
  </a-modal>
</template>

<script setup lang="ts">
  import { ref, onMounted, watch } from 'vue';
  import { DocRes, queryDocAll } from '@/api/doc';
  //   import { result } from 'lodash';
  import { useRouter } from 'vue-router';

  const visible = ref(false);
  const showHistory = ref(false);
  const historyItems = ref<string[]>([]);
  const searchResults = ref<DocRes[]>([]);
  const searchQuery = ref('');
  const router = useRouter(); // 使用 Vue Router

  const handleClick = () => {
    visible.value = true;
    showHistory.value = !searchQuery.value;
  };

  const handleOk = () => {
    visible.value = false;
  };

  const handleCancel = () => {
    visible.value = false;
  };

  const handleInput = async () => {
    if (!searchQuery.value) {
      showHistory.value = true;
    } else {
      showHistory.value = false;
      try {
        const results = await queryDocAll({ title: searchQuery.value });
        searchResults.value = results;
      } catch (error) {
        // console.error('搜索失败:', error);
      }
    }
  };

  const handleEnter = () => {
    if (searchQuery.value) {
      // 如果搜索历史中已经存在该记录，则先删除它
      const index = historyItems.value.indexOf(searchQuery.value);
      if (index !== -1) {
        historyItems.value.splice(index, 1);
      }
      // 将新记录插入到数组的第一个位置
      historyItems.value.unshift(searchQuery.value);

      // 只保留最多5条历史记录
      if (historyItems.value.length > 5) {
        historyItems.value = historyItems.value.slice(0, 5);
      }

      localStorage.setItem('searchHistory', JSON.stringify(historyItems.value));
    }
  };
  const historyHandle = (item: any) => {
    searchQuery.value = item;
    handleEnter();
    handleInput();
  };

  const clearHistory = () => {
    historyItems.value = [];
    localStorage.removeItem('searchHistory');
  };

  const deleteHistoryItem = (index: number) => {
    historyItems.value.splice(index, 1);
    localStorage.setItem('searchHistory', JSON.stringify(historyItems.value));
  };

  const loadSearchHistory = () => {
    const storedHistory = localStorage.getItem('searchHistory');
    if (storedHistory) {
      historyItems.value = JSON.parse(storedHistory);
    }
  };

  // 在组件挂载时加载历史搜索记录
  onMounted(loadSearchHistory);

  // 计算过滤后的搜索结果
  const filteredResults = ref<DocRes[]>([]);
  watch([searchQuery, searchResults], () => {
    if (searchQuery.value) {
      filteredResults.value = searchResults.value.filter((result) =>
        result?.title?.includes(searchQuery.value)
      );
    } else {
      filteredResults.value = [];
    }
  });

  // 搜索结果跳转
  const handleResultClick = (id: any) => {
    // router.push({ name: 'appClientMenus', params: { id } });
    router.push({
      name: 'DataDocDetail',
      query: { docId: id },
    });
    handleEnter();
    visible.value = false;
  };
</script>

<style scoped lang="less">
  .nav-btn {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-title {
    width: 100%;
  }

  .search {
    position: relative;
    width: 100%;
    background-color: transparent;
    border: none;
    box-shadow: none;
  }

  .search:focus {
    outline: none;
    box-shadow: none;
  }
  .del {
    cursor: pointer;
    color: rgb(22, 93, 255);
  }
  .time {
    margin-left: 15px;
  }
  .history,
  .searchResults {
    width: 100%;
    height: 100%;
  }

  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .history-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
  }

  .history-item:hover,
  .ResultItem:hover {
    // background-color: #f0f0f0;
    opacity: 1.5;
    cursor: pointer;
    color: rgb(22, 93, 255);
  }

  .delete-icon {
    float: right;
    cursor: pointer;
    display: none;
    color: rgb(22, 93, 255);
  }

  .history-item:hover .delete-icon {
    display: block;
  }

  .history {
    margin-top: 0;
  }

  .searchResults {
    margin-top: 0;
  }
</style>
