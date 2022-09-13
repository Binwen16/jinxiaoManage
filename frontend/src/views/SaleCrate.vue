<template>
  <div>
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>开票</span>
      </div>
      <div class="body">
        <el-form
          :model="ruleForm"
          :rules="rules"
          ref="ruleForm"
          label-width="100px"
          class="demo-ruleForm"
        >
          <div class="box">
            <div class="com">
              <el-form-item label="盘点单编号" prop="saleid">
                <el-input v-model="ruleForm.saleid"></el-input>
              </el-form-item>
              <el-form-item label="客户名称" prop="name">
                <el-input v-model="ruleForm.name"></el-input>
              </el-form-item>
            </div>
            <div class="com">
              <el-form-item label="时间" prop="time">
                <div class="block">
                  <span class="demonstration"></span>
                  <el-date-picker
                    v-model="ruleForm.time"
                    format="yyyy-MM-dd"
                    value-format="yyyy-MM-dd"
                    type="datetime"
                    placeholder="选择日期时间"
                  >
                  </el-date-picker>
                </div>
              </el-form-item>
              <el-form-item label="开单人" prop="sale">
                <el-select v-model="ruleForm.sale">
                  <el-option
                    v-for="item in staff"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  >
                  </el-option>

                </el-select>
              </el-form-item>
            </div>
          </div>
          <el-form-item label="订单明细" prop="delivery">
            <div id="orderTest">
              <el-dialog title="产品库" :visible.sync="dialogTableVisible">
                <el-table :data="list">
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
                  <el-table-column
                    prop="total_quantity"
                    label="可用数量"
                  ></el-table-column>
                  <el-table-column
                    :context="_self"
                    inline-template
                    label="操作"
                  >
                    <template slot-scope="scope">
                      <el-button
                        type="primary"
                        size="small"
                        @click="choise(scope.row)"
                      >
                        选择
                      </el-button>
                    </template>

                    <div></div>
                  </el-table-column>
                </el-table>
              </el-dialog>

              <el-button
                type="info"
                icon="view"
                @click="dialogTableVisible = true"
                >选择产品</el-button
              >

              <el-table :data="checkedNames" v-show="checkedNames.length > 0">
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
                      v-model="scope.row.num"
                      size="mini"
                      :min="1"
                      :max="10"
                      label="描述文字"
                    ></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column :context="_self" label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="del(scope.row)"
                      >删除</el-button
                    >
                  </template>
                </el-table-column>
              </el-table>
              <el-col :span="6" :offset="20">
                <span
                  v-show="checkedNames.length > 0"
                  style="font-family: Microsoft YaHei"
                  class="zongjai"
                  >总价：{{ sumPrice }}元
                </span>
              </el-col>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')"
              >立即创建</el-button
            >
            <el-button @click="resetForm('ruleForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getGoodBalanceListAPI } from '@/api/GoodBalanceListAPI.js'
import { SaleOrderCreat } from '@/api/Sale.js'
import { getStaff } from '@/api/staff.js'
export default {
  data() {
    return {
      dialogTableVisible: false,
      staff: [],
      list: [],
      checkedNames: [],
      ruleForm: {
        saleid: '',
        name: '',
        time: '',
        sale:'',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
      rules: {
        name: [
          { required: true, message: '请输入活动名称', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 5 个字符', trigger: 'blur' },
        ],
        saleid: [
          { required: true, message: '请选择活动区域', trigger: 'change' },
        ],
        time: [
          {
            required: true,
            message: '请选择日期',
            trigger: 'change',
          },
        ],
        type: [
          {
            type: 'array',
            required: true,
            message: '请至少选择一个活动性质',
            trigger: 'change',
          },
        ],
        resource: [
          { required: true, message: '请选择活动资源', trigger: 'change' },
        ],
        desc: [{ required: true, message: '请填写活动形式', trigger: 'blur' }],
      },
    }
  },
  created() {
    this.initGoodBalanceList()
    this.initStaffList()
  },
  computed: {
    sumPrice: function () {
      var sum = 0
      for (var i = 0; i < this.checkedNames.length; i++) {
        sum += this.checkedNames[i].good_price * this.checkedNames[i].num
      }
      return sum
    },
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(this.ruleForm.time);
          let formData = {
            number: this.ruleForm.saleid,
            handle_time: this.ruleForm.time,
            customerName: this.ruleForm.name,
            drawer:this.ruleForm.sale,
            sales_goods_items: this.checkedNames.map((item) => {
              return {
                goods: item.goods,
                sales_quantity: item.num,
              }
            }),
          }
          SaleOrderCreat(formData)
            .then((data) => {
              console.log(666)
              this.$message.success('创建成功')
              this.$router.push({ path: '/sale/' })
            })
            .finally(() => {
              this.loading = false
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.checkedNames = []
    },
    choise: function (p) {
      this.checkedNames.push(p)
    },
    del: function (p) {
      
      this.checkedNames.splice(p, 1)
      
    },
    async initGoodBalanceList() {
      // const res = await axios.get('http://127.0.0.1:8000/goods_balance/')
      const {
        data: { results: res }
      } = await getGoodBalanceListAPI()

      this.list = res
      // console.log(res);
    },
    async initStaffList() {
      // const res = await axios.get('http://127.0.0.1:8000/goods_balance/')
      const {
        data: { results: res },
      } = await getStaff()

      this.staff = res
      
    },
  },
}
</script>

<style lang="less" scoped>
/deep/.el-input-number .el-input__inner {
  width: 130px;
}
.el-dialog {
  width: 80%;
}
.zongjai {
  left: 0vh;
}
.box {
  display: flex;
  flex-wrap: wrap;
  align-content: space-between;
}

.com {
  flex-basis: 85%;
  display: flex;
  justify-content: space-between;
}
.col1 {
  display: flex;
}
</style>
