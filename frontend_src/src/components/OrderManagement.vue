<!-- <template>
  <div>
    <h2>My Orders</h2>
    <div v-for="order in orders" :key="order.id">
      <p>Order ID: {{ order.id }}, Total: ${{ order.total_price }}, Status: {{ order.status }}, Date: {{ new Date(order.order_date).toLocaleDateString() }}</p>
      <ul>
        <li v-for="detail in order.order_details" :key="detail.product_name">
          Product: {{ detail.product_name }}, Quantity: {{ detail.quantity }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: []
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      axios.get('http://localhost:8000/api/shop/my_orders/', { withCredentials: true })
        .then(response => {
          this.orders = response.data;
        })
        .catch(error => console.error("Error fetching orders:", error));
    }
  }
}
</script> -->

<template>
  <div class="orders-container">
    <h2>My Orders</h2>
    <div class="order" v-for="order in orders" :key="order.id">
      <p>Order ID: {{ order.id }}, Total: ${{ order.total_price }}, Status: {{ order.status }}, Date: {{ new Date(order.order_date).toLocaleDateString() }}</p>
      <ul>
        <li v-for="detail in order.order_details" :key="detail.product_name" class="order-detail">
          Product: {{ detail.product_name }}, Quantity: {{ detail.quantity }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: []
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      axios.get('http://localhost:8000/api/shop/my_orders/', { withCredentials: true })
        .then(response => {
          this.orders = response.data;
        })
        .catch(error => console.error("Error fetching orders:", error));
    }
  }
}
</script>

<style scoped>
.orders-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.order {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.order-detail {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 4px;
  margin: 5px 0;
  list-style-type: none; /* Remove default list bullet */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
