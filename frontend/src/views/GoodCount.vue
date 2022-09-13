<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>货物盘点</span>
    </div>

    <div class="table">
      <div class="search-Box">
        <el-input
          placeholder="请输入关键字"
          icon="search"
          width="100px"
          class="search"
          v-model="search"
        ></el-input>
        <el-button
          type="primary"
          size="mini"
          icon="el-icon-plus"
          @click="addGoodCountList"
          >新增盘点</el-button
        >
      </div>
      <el-table :data="tables" border style="width: 100%">
        <el-table-column type="index" width="50"> </el-table-column>
        <el-table-column prop="numbers" label="盘点单号"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="operator_name" label="盘点人"></el-table-column>


      </el-table>
    </div>
  </el-card>
</template>
<script>
import { GoodsCount } from '@/api/Good.js'
export default {
  data() {
    return {
      search: '', //搜索
      goodcountlist: [],
    }
  },
  created() {
    this.initGoodCountList()
  },
  computed: {
    tables: function () {
      var search = this.search
      if (search) {
        return this.goodcountlist.filter(function (dataNews) {
          return Object.keys(dataNews).some(function (key) {
            return String(dataNews[key]).toLowerCase().indexOf(search) > -1
          })
        })
      }
      return this.goodcountlist
    },
  },
  methods: {
    addGoodCountList() {
      this.$router.push({
        name: 'addgoodcount',
      })
    },
    async initGoodCountList() {

      const {
        data: { results: res },
      } = await GoodsCount()
      this.goodcountlist = res
      console.log(res);

    },
  },
}
</script>

<style>
.search-Box {
  margin-bottom: 10px;
  display: flex;
  justify-content: start;
}
.el-input__inner {
  width: 200px;
}
</style>
