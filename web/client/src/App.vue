<template>
  <div>
    <Header></Header>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from '@/components/Header'

export default {
    components: {Header},
}
</script>

<style>
* { 
  padding: 0;
  margin: 0;
}

*, *::before, *::after {
  box-sizing: inherit;
}

html, body {
    min-height: 100% !important;
    height: 100%;
}

</style>