<template>
  <div>
    <button @click="comName = 'Left'">展示Left组件</button>
    <button @click="comName = 'Right'">展示Right组件</button>
    <!-- component内置的 -->
    <keep-alive include="Left">
      <component :is="comName"></component>
    </keep-alive>
    
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
    return { comName: 'Left' }
  },

}
</script>

<style></style>
