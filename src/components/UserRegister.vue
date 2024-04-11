<template>
  <div class="register-container">
    <form @submit.prevent="register" class="register-form">
      <h2>Register</h2>
      <input class="input-field" v-model="username" placeholder="Username">
      <input class="input-field" v-model="email" placeholder="Email">
      <input class="input-field" type="password" v-model="password" placeholder="Password">
      <button type="submit" class="submit-btn">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    register() {
      const data = {
        username: this.username,
        email: this.email,
        password: this.password
      };
      axios.post('http://localhost:8000/api/shop/register/', data)
        .then(() => this.$router.push('/login'))
        .catch(error => {
          let errorMessage = "Error during registration.";
          if (error.response && error.response.data && error.response.data.error) {
              errorMessage += ` ${error.response.data.error}`;
          }
          console.error(errorMessage);
          alert(errorMessage);
        });      
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.register-form {
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
