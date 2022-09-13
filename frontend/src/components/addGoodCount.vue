<template>
  <div>
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>新增货物盘点单</span>
        <el-button size="mini" icon="el-icon-arrow-left" style="float: right; padding: 3px 0" type="text" @click=$router.go(-1)>返回</el-button>
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
              <el-form-item label="盘点编号" prop="goodcountid">
                <el-input v-model="ruleForm.goodcountid"></el-input>
              </el-form-item>

            </div>
            <div class="com">
              <el-form-item label="时间" prop="time">
                <div class="block">
                  <span class="demonstration"></span>
                  <el-date-picker
                    v-model="ruleForm.time"
                    type="datetime"
                    format="yyyy-MM-dd"
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期时间"
                  >
                  </el-date-picker>
                </div>
              </el-form-item>
              <el-form-item label="盘点人" prop="operator">
                <el-select v-model="ruleForm.operator">
                  <el-option
                    v-for="item in operator"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </div>
          </div>
          <el-form-item label="货物盘点明细" prop="delivery">
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
                  prop="total_quantity"
                  label="账面数量"
                ></el-table-column>

                <el-table-column label="实际数量" width="200">
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
import { GoodCountCreat } from '@/api/Good.js'
import { getStaff } from '@/api/staff.js'
export default {
  data() {
    return {
      dialogTableVisible: false,
      checkedNames: [],
      operator: [],
      list: [],
      ruleForm: {
        goodcountid: '',
        time: '',
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
          { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' },
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
    this.initoperatorList()
  },
  computed: {

  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let formData = {
            numbers: this.ruleForm.goodcountid,
            date: this.ruleForm.time,
            operator:this.ruleForm.operator,
            good_count_items: this.checkedNames.map((item) => {
              return {
                goods: item.goods,
                actual_goods: item.num,
              }
            }),
          }
          GoodCountCreat(formData)
            .then((data) => {
              console.log(666)
              this.$message.success('创建成功')
              this.$router.push({ path: '/goodcount/' })
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

      const {
        data: { results: res },
      } = await getGoodBalanceListAPI()

      this.list = res
      
    },
    async initoperatorList() {
  
      const {
        data: { results: res },
      } = await getStaff()

      this.operator = res
      
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
  flex-basis:85%;
  display: flex;
  justify-content: space-between;
}
.col1 {
  display: flex;
}
</style>
