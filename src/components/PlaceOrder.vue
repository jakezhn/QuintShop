<template>
  <div class="order-container">
    <h2>Place Order</h2>
    <div class="product-selection" v-for="product in products" :key="product.id">
      <input type="checkbox" :value="product.id" v-model="selectedProducts" @change="updateTotalPrice">
      {{ product.name }} - ${{ product.price }}
      <select v-model="quantities[product.id]" @change="updateTotalPrice" class="quantity-select">
        <option v-for="n in 10" :value="n" :key="n">{{ n }}</option>
      </select>
    </div>
    <p>Total Price: ${{ totalPrice }}</p>
    <button @click="placeOrder" class="place-order-btn">Place Order</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
      selectedProducts: [],
      quantities: {},
      totalPrice: 0,
    };
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      axios.get('http://localhost:8000/api/shop/products/')
        .then(response => {
          this.products = response.data;
          // Initialize quantities and apply initial total price calculation
          this.products.forEach(product => {
              this.quantities[product.id] = 1;
          });
          this.updateTotalPrice(); // Initial total price calculation
        })
        .catch(error => console.error("Error fetching products: ", error));
    },
    updateTotalPrice() {
      this.totalPrice = this.selectedProducts.reduce((total, productId) => {
        const product = this.products.find(p => p.id === parseInt(productId));
        const quantity = this.quantities[productId];
        // Assuming the discount is a percentage value; adjust the formula if needed
        const price = product.price * quantity * (1 - (product.discount / 100)).toFixed(2);
        return total + parseFloat(price);
      }, 0).toFixed(2);
    },
    placeOrder() {
      const items = this.selectedProducts.map(productId => {
        const product = this.products.find(p => p.id === parseInt(productId));
        return {
          product_id: productId,
          quantity: this.quantities[productId],
          price: product.price, // Send the original price; let backend handle discount
        };
      });
      const data = {
        items: items,
        total_price: parseFloat(this.totalPrice), // Ensure this is a float
      };
      axios.post('http://localhost:8000/api/shop/place_order/', data, { withCredentials: true }) // Ensure withCredentials is set if needed
        .then(() => {
          alert('Order placed successfully!');
          this.$router.push('/');
        })
        .catch(error => {
          if (localStorage.getItem('isAdmin') === '1') {
            alert('Only customer can place an order!');
          }
          console.error("Error placing order: ", error)
        });
    },
  },
}
</script>

<style scoped>
.order-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-selection {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.quantity-select {
  padding: 5px;
  margin-left: 10px;
}

.place-order-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px; /* Ensure some space between the total price and the button */
}

.place-order-btn:hover {
  background-color: #0056b3;
}
</style>
