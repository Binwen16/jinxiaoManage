<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>货物余额</span>


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
          @click="addGoobalanceList"
          >新增货物
    </el-button>
      </div>
      <el-table :data="tables" border style="width: 100%">
        <el-table-column type="index" width="50"> </el-table-column>
        <el-table-column prop="good_brand" label="品牌"></el-table-column>
        <el-table-column prop="good_model" label="规格"> </el-table-column>
        <el-table-column
          prop="good_specifications"
          label="型号"
        ></el-table-column>
        <el-table-column
          prop="good_serial_number"
          label="序列号"
        ></el-table-column>
        <el-table-column prop="unit_name" label="单位"></el-table-column>
        <el-table-column
          prop="total_quantity"
          label="可用数量"
        ></el-table-column>
      </el-table>
    </div>
  </el-card>
</template>
<script>

import { getGoodBalanceListAPI } from '@/api/GoodBalanceListAPI.js'


export default {
  data() {
    return {
      search: '', //搜索
      tableData: [], //表格内容
    }
  },
  created() {
    this.initGoodBalanceList()
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
    async initGoodBalanceList() {
      // const res = await axios.get('http://127.0.0.1:8000/goods_balance/')
      const {
        data: { results: res },
      } = await getGoodBalanceListAPI()

      this.tableData = res
      // console.log(res)
    },
    addGoobalanceList(){
      this.$router.push({
        name: 'addgood',
      })
    }
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
