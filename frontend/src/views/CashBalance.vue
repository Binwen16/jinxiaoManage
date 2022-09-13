<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>现金余额</span>
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
      </div>
      <el-table :data="tables" border style="width: 100%">
        <el-table-column type="index" width="50"> </el-table-column>
        <el-table-column prop="data" label="日期"></el-table-column>
        <el-table-column prop="entry_name" label="摘要"> </el-table-column>
        <el-table-column
          prop="debit_amount"
          label="开支"
        ></el-table-column>
        <el-table-column
          prop="credit_amount"
          label="收入"
        ></el-table-column>
        <el-table-column prop="cumulative" label="余额"></el-table-column>
      </el-table>
    </div>
  </el-card>
</template>
<script>
import { CashBalance } from '@/api/Cash.js'

export default {
  data() {
    return {
      search: '', //搜索
      tableData: [], //表格内容
    }
  },
  created() {
    this.initCashBalanceList()
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
    async initCashBalanceList() {
      const {
        data: { results: res },
      } = await CashBalance()

      this.tableData = res
      console.log(res)
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
