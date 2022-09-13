<template>
  <div class="Left-container">
    <h3>Left</h3>
    <div>
      <p>{{ msg }}</p>
      <hr />
      <button @click="count += 1">{{ count }}</button>
      <p>{{ id }}</p>
      <slot name="fa" :msg1=count :user="userinfo"></slot>
      <button @click="changecount">改变名字</button>
      <button @click="thischnage">动态绑定this</button>
    </div>
  </div>
</template>

<script>
export default {
  created() {
    console.log('Left 组件被创建')
  },
  destroyed() {
    console.log('Left 组件被销毁')
  },
  activated() {
    console.log('Left 组件被激活,触发activated')
  },
  deactivated() {
    console.log('Left 组件被缓存,触发deactivated')
  },
  props: ['msg', 'id'],
  data() {
    return {
      count: 0,
      userinfo:{
        "name":"zs",
        "sge":"ls",
      }
    }
  },
  methods:{
    changecount(){
      this.count++
    },
    thischnage(){
      console.log(this);
    }
  }
}
</script>

<style lang="less" scoped>
.Left-container {
  background-color: pink;
  min-height: 200px;
  flex: 1;
}
</style>
