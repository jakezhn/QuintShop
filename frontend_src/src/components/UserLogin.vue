<template>
  <div class="login-container">
    <form @submit.prevent="login" class="login-form">
      <h2>Login</h2>
      <input class="input-field" v-model="username" placeholder="Username">
      <input class="input-field" type="password" v-model="password" placeholder="Password">
      <button type="submit" class="submit-btn">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      const data = {
        username: this.username,
        password: this.password
      };
      axios.post('http://localhost:8000/api/shop/login/', data)
        .then(response => {
          // Store login state
          localStorage.setItem('loggedIn', '1');
          localStorage.setItem('username', data.username);

          // Check the role and redirect accordingly
          if (response.data.role === 'admin') {
            localStorage.setItem('isAdmin', '1');
            this.$router.push('/admin');
          } else{
            this.$router.push('/');
          }
        })
        .catch(error => {
          console.error("Login failed: ", error);
          // Handle login failure (e.g., show an error message)
        });
    }
  }
}  
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 10px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.input-field {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 16px;
}

.submit-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>
