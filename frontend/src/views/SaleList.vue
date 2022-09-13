<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>小票收款发货</span>
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
        <el-table-column prop="number" label="小票号"></el-table-column>
        <el-table-column prop="handle_time" label="时间"> </el-table-column>
        <el-table-column prop="customerName" label="顾客名称">
        </el-table-column>
        <el-table-column prop="state" label="状态"> </el-table-column>
        <el-table-column prop="drawer_name" label="开单人"> </el-table-column>
        <el-table-column prop="payee_name" label="收款人"> </el-table-column>
        <el-table-column prop="consignor_name" label="发货人">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
              >编辑</el-button
            >
            <div id="orderTest">
              <el-dialog title="小票修改" :visible.sync="dialogTableVisible">
                <el-card class="box-card">
                  <div slot="header" class="clearfix">
                    <span>{{ changeData.number }}小票明细</span>
                  </div>
                  <el-row :gutter="10">
                    <el-form ref="form" :model="form" label-width="80px">
                      <el-col
                        :span="6"
                        style="width: 100%; margin-bottom: 10px"
                      >
                        <el-form-item label="小票号">
                          <el-input
                            v-model="changeData.number"
                            :disabled="true"
                          >
                          </el-input>
                        </el-form-item>
                      </el-col>

                      <el-col :span="6" style="width: 100%">
                        <el-form-item label="小票状态" prop="state">
                          <el-select v-model="changeData.state">
                            <el-option
                              v-for="item in saleordelsate"
                              :key="item.id"
                              :label="item.name"
                              :value="item.name"
                            >
                            </el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>

                      <el-col :span="6" style="width: 320px">
                        <el-form-item label="开单人" prop="sale">
                          <el-select v-model="changeData.drawer">
                            <el-option
                              v-for="item in staff"
                              :key="item.id"
                              :label="item.name"
                              :value="item.id"
                            >
                            </el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="6" style="width: 320px">
                        <el-form-item label="收款人" prop="payee">
                          <el-select v-model="changeData.payee">
                            <el-option
                              v-for="item in staff"
                              :key="item.id"
                              :label="item.name"
                              :value="item.id"
                            >
                            </el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col :span="6" style="width: 320px">
                        <el-form-item label="发货人" prop="consignor">
                          <el-select v-model="changeData.consignor">
                            <el-option
                              v-for="item in staff"
                              :key="item.id"
                              :label="item.name"
                              :value="item.id"
                            >
                            </el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>
                      <el-col>
                        <el-form-item label="总金额" style="width: 320px">
                          <el-input
                            v-model="changeData.total_amount"
                            :disabled="true"
                          >
                          </el-input>
                        </el-form-item>
                      </el-col>
                    </el-form>
                  </el-row>

                  <el-table :data="SaleOrderdetial[0]">
                    <el-table-column type="index" width="75"> </el-table-column>
                    <el-table-column
                      prop="good_brand"
                      label="品牌"
                    ></el-table-column>
                    <el-table-column prop="good_model" label="规格">
                    </el-table-column>
                    <el-table-column
                      prop="good_specifications"
                      label="型号"
                    ></el-table-column>
                    <el-table-column
                      prop="good_serial_number"
                      label="序列号"
                    ></el-table-column>
                    <el-table-column
                      prop="unit_name"
                      label="单位"
                    ></el-table-column>
                    <el-table-column
                      prop="good_price"
                      label="价格"
                    ></el-table-column>
                    <el-table-column label="数量" width="200px">
                      <template slot-scope="scope">
                        <el-input-number
                          v-model="scope.row.sales_quantity"
                          size="mini"
                          :min="1"
                          :max="10"
                          label="描述文字"
                        ></el-input-number>
                      </template>
                    </el-table-column>
                    <el-table-column :context="_self" label="操作">
                      <template slot-scope="scope">
                        <el-button
                          size="mini"
                          type="danger"
                          @click="del(scope.row)"
                          >删除</el-button
                        >
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="dialogTableVisible = false"
                    >取 消</el-button
                  >
                  <el-button type="primary" @click="changesaleordel"
                    >确 定</el-button
                  >
                </div>
              </el-dialog>
            </div>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination
  background
  layout="prev, pager, next"
  :total="20">
</el-pagination>
  </el-card>
</template>
<script>
import { SaleOrder, SaleOrderUpdate } from '@/api/Sale.js'
import { getStaff } from '@/api/staff.js'

export default {
  data() {
    return {
      number: '',
      sale: '',
      payee: '',
      consignor: '',
      state: '',

      
      list: [],
      staff: [],
      dialogTableVisible: false,
      search: '', //搜索
      tableData: [], //表格内容
      changeData: [],
      SaleOrderdetial: [],
      form: {},
      saleordelsate: [
        { id: 1, name: '未付款未发货' },
        { id: 2, name: '已收款' },
        { id: 3, name: '已发货' },
      ],
    }
  },
  created() {
    this.initSaleOrderList()
    this.initStaffList()
  },

  mounted() {},

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
    async initSaleOrderList() {
      const {
        data: { results: res },
      } = await SaleOrder()

      this.tableData = res
    },
    handleEdit(data1, data2) {
      this.dialogTableVisible = true
      // console.log(data2);
      this.changeData = data2
      this.SaleOrderdetial = [data2.sales_goods_items]
      // console.log(this.staff)
    },
    async initStaffList() {
      // const res = await axios.get('http://127.0.0.1:8000/goods_balance/')
      const {
        data: { results: res },
      } = await getStaff()

      this.staff = res
      this.staff.unshift({ id: '', name: '无' })
      // console.log(this.staff);
    },

    changesaleordel() {
      
      let formData = {
        id: this.changeData.id,
        payee: this.changeData.payee,
        consignor: this.changeData.consignor,
        drawer: this.changeData.drawer,
        state: this.changeData.state,
      }
      console.log(this.changeData);
      SaleOrderUpdate(formData)
        .then((data) => {
          console.log(666)
          this.$message.success('修改成功')
          this.$router.push({ path: '/salelist/' })
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>

<style lang="less" scoped>
  .el-pagination{
    float: right;
    margin-top: 10px;
  }
.demo-input-suffix {
  display: flex;
}
/deep/.el-input-number .el-input__inner {
  width: 130px;
}
/deep/.el-dialog {
  width: 90%;
}
.search-Box {
  margin-bottom: 10px;
  display: flex;
  justify-content: start;
}
.el-input__inner {
  width: 200px;
}
</style>
