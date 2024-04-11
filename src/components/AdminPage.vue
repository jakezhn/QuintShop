<template>
  <div class="home">
    <h1>Welcome to Admin Console!</h1>
    <p>You can manage products, orders, transactions, and support tickets here.</p>

    <div class="actions">
      <router-link to="/admin/products" class="button">Product Management</router-link>
      <router-link to="/admin/orders" class="button">Orders Management</router-link>
      <router-link to="/admin/support_tickets" class="button">Support Tickets Management</router-link>
      <router-link to="/admin/transactions" class="button">View Transactions</router-link>
      <button @click="logout" class="button logout">Logout</button>
    </div>
  </div>
</template>

<script>
//import axios from 'axios';

export default {
    data() {
        return {
            isLoggedIn: localStorage.getItem('loggedIn') === '1',
        };
    },
    methods: {
        logout() {
            localStorage.setItem('loggedIn', '0');
            localStorage.removeItem('username');
            localStorage.removeItem('isAdmin');

            this.$router.push('/');
        },
    }
}
</script>

<style>
.home h1 {
  text-align: center;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px; /* Adds space between buttons */
  margin-top: 20px;
}
.button, .logout {
  text-decoration: none;
  color: white;
  background-color: #007bff;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
.logout {
  background-color: #007bff; /* Different color for logout for distinction */
}
.button:hover, .logout:hover {
  opacity: 0.8;
}
</style>
