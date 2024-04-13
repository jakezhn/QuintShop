
<template>
  <div class="product-container">
    <h1>Products</h1>
    <div class="search-box">
      <input v-model="searchQuery" placeholder="Search products" class="search-input" @keyup.enter="fetchProducts(true)"/>
      <button @click="fetchProducts(true)" class="search-btn">Search</button>
    </div>
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
      searchQuery: '',
    };
  },
  mounted() {
    this.fetchProducts(false); // Load all products initially
  },
  methods: {
    fetchProducts(searchInitiated) {
      if (!searchInitiated && !this.searchQuery) {
        // Load all products if no search has been initiated and no search query is present
        axios.get('http://localhost:8000/api/shop/products/')
          .then(response => {
            this.products = response.data;
          })
          .catch(error => this.handleError(error));
      } else if (this.searchQuery) {
        // Conduct a search only if there is a query
        axios.get(`http://localhost:8000/api/shop/product_search/?search=${encodeURIComponent(this.searchQuery.trim())}`)
          .then(response => {
            this.products = response.data;
            console.log('Received products:', response.data);

            console.log(`URL Requested: http://localhost:8000/api/shop/product_search/?search=${encodeURIComponent(this.searchQuery.trim())}`);

          })
          .catch(error => this.handleError(error));
      }
    },
    viewProduct(productId) {
      this.$router.push({ name: 'ProductDetail', params: { id: productId } });
    },
    handleError(error) {
      let errorMessage = "Error listing products.";
      if (error.response && error.response.data && error.response.data.error) {
          errorMessage += ` ${error.response.data.error}`;
      }
      console.error(errorMessage);
      alert(errorMessage);
    },
  },
}
</script>

<style scoped>
.product-container {
  max-width: 960px;
  margin: auto;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-box {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.search-input {
  width: 70%;
  padding: 10px 15px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 20px;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #007bff;
  outline: none;
}

.search-btn {
  padding: 10px 20px;
  margin-left: 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #0056b3;
}

.product-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.product-item {
  background-color: #ffffff;
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: calc(33.333% - 20px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 10px rgba(0,0,0,0.15);
}

.view-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.view-btn:hover {
  background-color: #007bff;
}
</style>

