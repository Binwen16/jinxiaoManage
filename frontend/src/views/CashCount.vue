<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>现金盘点</span>
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
          @click="addCashCountList"
          >新增盘点</el-button
        >
      </div>
      <el-table :data="tables" border style="width: 100%">
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="numbers" label="盘点单号"> </el-table-column>
        <el-table-column prop="book_cash" label="账面"></el-table-column>
        <el-table-column prop="actual_cash" label="实际金额"></el-table-column>
        <el-table-column prop="Profit_loss" label="盈余"></el-table-column>
        <el-table-column prop="operator_name" label="出纳员"></el-table-column>
      </el-table>
    </div>
  </el-card>
</template>
<script>
import { CashCount } from '@/api/Cash.js'
export default {
  data() {
    return {
      search: '', //搜索
      tableData: [], //表格内容
    }
  },
  created() {
    this.initCashCountList()
  },
  computed: {
    tables: function () {
      var search = this.search
      if (search) {
        return this.tableData.filter(function (dataNews) {
          return Object.keys(dataNews).some(function (key) {
            return String(dataNews[key]).toLowerCase().indexOf(search) > -1
          })
        })
      }
      return this.tableData
    },
  },
  methods: {
    async initCashCountList() {
      const {
        data: { results: res },
      } = await CashCount()

      this.tableData = res
      console.log(res);
    },
    addCashCountList() {
      this.$router.push({
        name: 'addcashcount',
      })
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
