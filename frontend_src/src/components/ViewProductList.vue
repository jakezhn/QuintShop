<template>
  <div class="product-container">
    <h1>Products</h1>
    <ul class="product-list">
      <li v-for="product in products" :key="product.id" class="product-item">
        {{ product.name }} - ${{ product.price }}
        <button @click="viewProduct(product.id)" class="view-btn">View</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      axios.get('http://localhost:8000/api/shop/products/')
        .then(response => (this.products = response.data))
        .catch(error => {
          let errorMessage = "Error listing product.";
          // Check if the error response has the specific message
          if (error.response && error.response.data && error.response.data.error) {
              errorMessage += ` ${error.response.data.error}`;
          }
          console.error(errorMessage);
          alert(errorMessage); // Display the constructed error message
        });
    },
    viewProduct(productId) {
      this.$router.push({ name: 'ProductDetail', params: { id: productId } });
    },
  },
}
</script>

<style scoped>
.product-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-btn {
  padding: 5px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.view-btn:hover {
  background-color: #0056b3;
}
</style>
