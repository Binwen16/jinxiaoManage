<template>
  <el-menu
    default-active="1-4-1"
    class="el-menu-vertical-demo"
    @open="handleOpen"
    @close="handleClose"
    :collapse="isCollapse"
  >
    <h3>{{isCollapse ? '15组': '15组手机店'}}</h3>
    <el-menu-item
      v-for="item in noChildren"
      :index="item.path + ''"
      :key="item.path"
      @click="clickMenu(item)"
    >
      <i :class="'el-icon-' + item.icon"></i>
      <span slot="title">{{ item.label }}</span>
    </el-menu-item>
    <el-submenu
      v-for="item in hasChildren"
      :index="item.path + ''"
      :key="item.path"
    >
      <template slot="title">
        <i :class="'el-icon-' + item.lcon"></i>
        <span slot="title">{{ item.ladel }}</span>
      </template>
      <el-menu-item-group
        v-for="(subItem, subIndex) in item.children"
        :key="subItem.path"
        
      >
        <el-menu-item :index="subIndex + ''" @click="clickMenuChilren(subItem)">{{ subItem.label }}</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  data() {
    return {
      menu: [
        {
          path: 'home',
          name: 'home',
          label: '首页',
          icon: 's-home',
          url: '',
        },
        {
          path: 'sale',
          name: 'sale',
          label: '开单',
          icon: 's-mall',
          url: 'MallManage/MallManage',
        },
        {
          path: 'salelist',
          name: 'salelist',
          label: '小票收款发货',
          icon: 's-mall',
          url: 'MallManage/MallManage',
        },
        {
          path: 'user',
          name: 'goodcount',
          label: '货物盘点',
          icon: 's-user',
          url: 'UserManage/UserManage',
        },
        {
          path: 'goodbalance',
          name: 'goodbalance',
          label: '货物余额',
          icon: 's-user',
          url: 'UserManage/UserManage',
        },
        {
          path: 'cashbalance',
          name: 'cashbalance',
          label: '现金余额',
          icon: 's-user',
          url: 'UserManage/UserManage',
        },
        {
          path: 'cashcount',
          name: 'cashcount',
          label: '现金盘点',
          icon: '',
          url: 'Other/PageTwo',
        },
        
      ],
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath)
    },
    clickMenuChilren(item) {
      console.log(this.hasChildren);
      console.log(item.name);
      this.$router.push({
        name: item.name,
      })
    },
    clickMenu(item) {
      console.log(this.hasChildren);
      console.log(item.name);
      this.$router.push({
        name: item.name,
      })
    },
  },
  computed: {
    noChildren() {
      return this.menu.filter((item) => !item.children)
    },
    
    hasChildren() {
      return this.menu.filter((item) => item.children)
    },
    isCollapse(){
      return this.$store.state.tab.isCollapse
    }
    
  },
}
</script>

<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.el-menu {
  height: 100%;
  bottom: none;

  h3 {
    color: black;
    text-align: center;
    line-height: 48px;
  }
}
</style>
