<template>
  <div class="home">
    <h1>Welcome to QuintShop!</h1>
    <p>Discover our amazing products!</p>

    <div class="featured-products">
      <h2>Featured Products</h2>
      <div class="product-list">
        <div v-for="product in featuredProducts" :key="product.id" class="product-item">
          <img :src="product.image_url" :alt="product.name" class="product-image">
          <h3>{{ product.name }}</h3>
          <p>Price: ${{ product.price }}</p>
          <router-link :to="{ name: 'ProductDetail', params: { id: product.id }}" class="view-detail-link">View Details</router-link>
        </div>
      </div>
    </div>

    <div class="actions">
      <router-link to="/register" class="button" v-if="!isLoggedIn">Register Now</router-link>
      <router-link to="/login" class="button" v-if="!isLoggedIn">Login</router-link>
      <button @click="logout" v-if="isLoggedIn" class="button">Logout</button>
      <router-link to="/place_order" class="button" v-if="isLoggedIn">Place Order</router-link>
      <router-link to="/my_orders" class="button" v-if="isLoggedIn">My Orders</router-link>
      <router-link to="/my_tickets" class="button" v-if="isLoggedIn">My Tickets</router-link>
      <router-link to="/products" class="button">Product List</router-link>
      <router-link to="/admin" class="button" v-if="isAdmin">Admin Console</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            featuredProducts: [],
            isLoggedIn: localStorage.getItem('loggedIn') === '1',
            isAdmin: localStorage.getItem('isAdmin') === '1',
        };
    },
    mounted() {
        this.fetchFeaturedProducts();
    },
    methods: {
        fetchFeaturedProducts() {
            axios.get('http://localhost:8000/api/shop/products/')
                .then(response => {
                    this.featuredProducts = response.data.filter(product => product.is_featured);
                })
                .catch(error => {
                    console.error("Error fetching featured products:", error);
                });
        },

        logout() {
            localStorage.setItem('loggedIn', '0');
            localStorage.removeItem('username');
            localStorage.removeItem('isAdmin');
            this.$router.push('/'); // Redirect to home page
            this.$nextTick(() => {
              window.location.reload();
            });
        },
    }
}
</script>

<style>
.home {
  text-align: center;
}

.featured-products, .actions {
  margin-top: 20px;
}

.product-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.product-item {
  width: 200px;
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  padding: 10px;
}

.product-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.view-detail-link {
  display: inline-block;
  margin-top: 10px;
  text-decoration: none;
  color: white;
  background-color: #007bff;
  padding: 5px 10px;
  border-radius: 4px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.button {
  text-decoration: none;
  color: white;
  background-color: #007bff;
  padding: 10px 20px;
  margin: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.button:hover {
  background-color: #0056b3;
}
</style>
