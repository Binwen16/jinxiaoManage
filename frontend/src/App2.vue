<template>
  <el-container>
    <el-aside width="auto">
      <NavMenu></NavMenu>
      
    </el-aside>
    <el-container>
      <el-header>
        <NavHeader></NavHeader>
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
// @ is an alias to /src
import NavMenu from '@/components/NavMenu.vue'
import NavHeader from '@/components/CommoHeader.vue'

export default {
  components: {
    NavMenu,
    NavHeader
  }
}
</script>
