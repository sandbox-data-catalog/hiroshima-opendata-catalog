<template>
  <div id="app">
    <Home />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Home from './Home.vue'

export default Vue.extend({
  name: 'App',
  components: {
    Home,
  },
})
</script>

<style lang="scss">
#app {
  text-align: center;
  width: 100%;
  overflow: visible;
  background: url('./assets/image/background.png') no-repeat;
  background-size: cover;
}

@media only screen and (min-width: 768px) {
  #app {
    min-height: 810px;
    height: 100%;
  }

  html,
  body {
    height: 100%;
  }
}
</style>
