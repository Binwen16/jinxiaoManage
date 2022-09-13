<template>
  <div class="body-contair">
    <h3 ref="myh3">MyTest</h3>
    <input type="text" v-if="inputVisible" />
    <button v-else @click="showInput" ref="ipt">展示input输入框</button>
    <button @click="getDOMRef">获取 DOM $refs 引用</button>
    <button @click="getcountRef">获取 counter $refs 引用</button>
    <div class="box">
      <Left ref="leftRef" :msg="title" :id="idd"></Left>
      <Right></Right>
    </div>
  </div>
</template>

<script>
import Left from './components/Left.vue'
import Right from './components/Right.vue'
export default {
  components: {
    Left,
    Right,
  },

  data(){
    return{
      inputVisible:false,
      title:'hello vue',
      idd:1
    }
  },
  methods: {
    // 通过 this.@refs.引用名称 可以获取到 DOM 元素的引用
    getDOMRef() {
      console.log(this.$refs.myh3) // this 是当前组件的实例对象， this.$refs 默认指向空对象			// 操作 DOM 元素，把文本原色改为红色
      this.$refs.myh3.style.color = 'red'
    },
    getcountRef() {
      // 通过 this.$refs.引用的名称 可以引用组件的实例
      console.log(this.$refs.counterRef)
      // 引用到组件的实例之后 就可以调用组件上的 methods 方法
    },
    showInput() {
      this.inputVisible=true
        // 把 input 文本框的操作推迟到下次 DOM 更新之后。否则页面上根本不存在文本框元素
      this.$nextTick(()=>{
        // 获取文本框的 DOM 引用，并调用 .foucus() 使其自动获得焦点
        this.$refs.ipt.focus()
      })
      
      
    }
  },
}
</script>

<style lang="less" scoped>
.box {
  display: flex;
  
}
</style>
