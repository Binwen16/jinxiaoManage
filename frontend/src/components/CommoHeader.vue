<template>
  <header>
    <div class="container">
      <el-button @click="handleMeun" plain icon="el-icon-menu" size="mini"></el-button>
      <div class="r-content">
        <el-dropdown trigger="click" size="mini">
          <span>
            <img :src="userImg" alt="" />
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item>推出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      userImg: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
    }
  },
  methods: {
    handleMeun(){
      this.$store.commit('collapseMenu')
    }
  }
}
</script>

<style lang="less" scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;

  img {
    height: 50px;
    width: 50px;
  }
}
</style>
