<template>
    <div>
        <div style="height: 400px;">
          <vue3-tree-org
            :data="data"
            center
            :horizontal="horizontal"
            :collapsable="collapsable"
            :label-style="style"
            :only-one-node="onlyOneNode"
            :clone-node-drag="cloneNodeDrag"
            :before-drag-end="beforeDragEnd"
            @on-node-drag="nodeDragMove"
            @on-node-drag-end="nodeDragEnd"
            @on-contextmenu="onMenus"
            @on-expand="onExpand"
            @on-node-dblclick="onNodeDblclick"
            @on-node-click="onNodeClick"
          />
        </div>
    </div>
  </template>
  <script>
  import { ref } from 'vue'
  import DATA from './orgTree'

  export default {
    name: "baseTree",
    setup() {
      const cloneNodeDrag = ref(true)
      return {
        cloneNodeDrag
      }
    },
    data() {
      return {
        data: DATA,
        horizontal: false,
        collapsable: true,
        onlyOneNode: false,
        expandAll: true,
        disaled: false,
        style: {
          background: "#fff",
          color: "#5e6d82",
        },
      };
    },
    created() {
      this.toggleExpand(this.data, this.expandAll);
    },
    methods: {
      onMenus({ node, command }) {
        console.log(node, command);
      },
      onExpand(e, data) {
        console.log(e, data);
      },
      onExpandAll(b) {
        console.log(b)
      },
      nodeDragMove(data) {
        console.log(data);
      },
      beforeDragEnd(node, targetNode) {
        return new Promise((resolve, reject) => {
          if (!targetNode) reject()
          if (node.id === targetNode.id) {
            reject()
          } else {
            resolve()
          }
        })
      },
      nodeDragEnd(data, isSelf) {
        console.log(data, isSelf);
      },
      onNodeDblclick() {
        console.log('onNodeDblclick')
      },
      expandChange() {
        // this.toggleExpand(this.data, this.expandAll);
      },
      toggleExpand(data, val) {
        if (Array.isArray(data)) {
          data.forEach((item) => {
            item.expand = val
            if (item.children) {
              this.toggleExpand(item.children, val);
            }
          });
        } else {
          data.expand = val
          if (data.children) {
            this.toggleExpand(data.children, val);
          }
        }
      },
    },
  };
  </script>
  