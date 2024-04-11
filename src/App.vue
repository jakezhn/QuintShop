<template>
  <div id="app">
    <!-- Navigation Bar or Links -->
    <nav>
      <router-link to="/">Home</router-link>
      <!-- Add more links for other routes here -->
    </nav>
    
    <!-- Router View -->
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav a {
  margin: 10px;
  text-decoration: none;
  color: #42b983; /* Vue green color for demonstration */
}
</style>
