<template>
    <div>
      <div style="margin-top:0px;width: calc(100% - 10px);height:calc(100vh);">
        <RelationGraph ref="graphRef" :options="graphOptions">
          <template #node="{node}">
            <div class="my-node-style" :style="{'background-image': 'url(' + node.data.icon + ')'}">
            </div>
            <div class="c-node-name" :style="{color:node.color}">{{node.text}}</div>
          </template>
        </RelationGraph>
      </div>
  
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted } from 'vue';
  import { getPreviewURL } from '@/utils/image';
  import RelationGraph, { RGJsonData, RGOptions, RGNode, RGLine, RGLink, RGUserEvent, RelationGraphComponent } from 'relation-graph-vue3';
  
  const props = defineProps({
    data: {
      type: Object,
      required: true,
    },
  });


  const graphOptions: RGOptions = {
    debug: false,
    defaultNodeBorderWidth: 0,
    defaultNodeColor: 'rgba(238, 178, 94, 1)',
    allowSwitchLineShape: true,
    allowSwitchJunctionPoint: true,
    defaultLineShape: 1,
    'layouts': [
      {
        'label': 'Auto Layout',
        'layoutName': 'force',
        'layoutClassName': 'seeks-layout-force'
      }
    ],
    defaultJunctionPoint: 'border',
    backgroundColor: '#1d2129',
  };
  
  const graphRef = ref<RelationGraphComponent>();
  const checked_sex = ref('');
  const checked_isgoodman = ref('');
  const rel_checkList = ref(['师生', '上下级', '亲戚', '情人', '朋友', '夫妻', '勾结', '腐化', '举报']);
  const all_rel_type = ref(['师生', '上下级', '亲戚', '情人', '朋友', '夫妻', '勾结', '腐化', '举报']);
  
  onMounted(() => {
      setGraphData();
  });
  
  const setGraphData = async () => {
      const __graph_json_data: RGJsonData = props.data as RGJsonData;
      const graphInstance = graphRef.value!.getInstance();
      __graph_json_data.nodes.forEach(thisNode => {
          const data = thisNode.data;
          if (data) {
            data.icon = getPreviewURL(data.icon);
          }
      })
      await graphInstance.setJsonData(__graph_json_data);
  };

  
  const doFilter = () => {
      const graphInstance = graphRef.value!.getInstance();
      const _all_nodes = graphInstance.getNodes();
      const _all_links = graphInstance.getLinks();
      _all_nodes.forEach(thisNode => {
          let _isHideThisLine = false;
          if (checked_sex.value !== '') {
              if (thisNode.data['sexType'] !== checked_sex.value) {
                  _isHideThisLine = true;
              }
          }
          if (checked_isgoodman.value !== '') {
              if (thisNode.data['isGoodMan'] !== checked_isgoodman.value) {
                  _isHideThisLine = true;
              }
          }
          thisNode.opacity = _isHideThisLine ? 0.1 : 1;
      });
      _all_links.forEach(thisLink => {
          thisLink.relations.forEach(thisLine => {
              if (rel_checkList.value.indexOf(thisLine.data['type']) === -1) {
                  if (!thisLine.isHide) {
                      thisLine.isHide = true;
                      console.log('Hide line:', thisLine);
                  }
              } else {
                  if (thisLine.isHide) {
                      thisLine.isHide = false;
                      console.log('Show line:', thisLine);
                  }
              }
          });
      });
      graphInstance.dataUpdated();
  };
  </script>
  
  <style lang="scss" scoped>
  .my-node-style{
    background-position: center center;
    background-size: 100%;
    height:100%;
    width:100%;
    border-radius: 40px;
    overflow: visible;
  }
  .c-node-name{
    width:80px;
    text-align:center;
    color: #2E74B5;
    margin-top: 10px;
  }
  
  </style>
  