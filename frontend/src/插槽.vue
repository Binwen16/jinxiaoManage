<template>
  <div>
    <button @click="comName = 'Left'">展示Left组件</button>
    <button @click="comName = 'Right'">展示Right组件</button>
    <h1 v-color="'red'">dddddd</h1>

    <Left>
      <!-- <template #fa="scope"> -->
      <template #fa="{ msg1, user }">
        <p>这是在Left组件中的p</p>
        <p>{{ msg1 }}</p>
        <p>{{ user.name }}</p>
      </template>
    </Left>
    <Right></Right>
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
  data() {
    return { comName: 'Left', list: [] }
  },
  directives: {
    // color:{
    //   // 当指令第一次被绑定到元素时被调用
    //   bind(el, binding){
    //     // 形参中的 el 是绑定了此指令的，原生的 DOM 对象
    //     el.style.color = binding.value
    //     console.log(3333);
    //   },
    //   // 每次DOM 更新时调用
    //   update(el,binding){
    //     el.style.color = binding.value
    //   }
    // }
    // color(el,binding){
    //   el.style.color = binding.value
    // }
  },

  created() {
    this.getAreaListFn()
  },
  methods: {
    getAreaListFn() {
      this.$axios
        .get('http://127.0.0.1:8000/article_detail')
        .then((response) => {
          
          this.list = response.data
          console.log(this.list)
        })
        .catch((response) => {
          console.log(this.list)
        })
    },
  },
}
</script>

<style></style>
