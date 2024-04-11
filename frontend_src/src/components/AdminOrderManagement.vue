<template>
  <div>
    <h2>Update Orders</h2>
    <select v-model="selectedOrderId" @change="fetchSelectedOrderDetails">
      <option disabled value="">Select an Order</option>
      <option v-for="order in orders" :key="order.id" :value="order.id">
        Order ID: {{ order.id }}
      </option>
    </select>

    <div v-if="selectedOrder">
      <h3>Order Details</h3>
      <p>Order ID: {{ selectedOrder.id }}</p>
      <p>Status: {{ selectedOrder.status }}</p>
      <p>Total Price: ${{ selectedOrder.total_price }}</p>
      <ul>
        <li v-for="detail in selectedOrderDetails" :key="detail.id">
          Product: {{ detail.product_name }}, Quantity: {{ detail.quantity }}, Price: ${{ detail.price_at_purchase }}
        </li>
      </ul>
      <select v-model="newStatus">
        <option disabled value="">Update Status</option>
        <option v-for="status in statusOptions" :key="status.value" :value="status.value">
          {{ status.text }}
        </option>
      </select>
      <button @click="updateOrderStatus">Update Status</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: [],
      selectedOrderId: '',
      selectedOrder: null,
      selectedOrderDetails: [],
      newStatus: '',
      statusOptions: [
        { value: 'Placed', text: 'Placed' },
        { value: 'Paid', text: 'Paid' },
        { value: 'Shipped', text: 'Shipped' },
        { value: 'Completed', text: 'Completed' },
        { value: 'Cancelled', text: 'Cancelled' }
      ]
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      axios.get('http://localhost:8000/api/shop/orders/')
        .then(response => (this.orders = response.data))
        .catch(error => console.error("Error fetching orders:", error));
    },
    fetchSelectedOrderDetails() {
      const selectedOrder = this.orders.find(order => order.id === this.selectedOrderId);
      this.selectedOrder = selectedOrder;
      // Assume you have an endpoint to fetch details for a specific order
      axios.get(`http://localhost:8000/api/shop/admin/orders/${this.selectedOrderId}/admin_view_orderdetials/`)
        .then(response => {
          this.selectedOrderDetails = response.data;
        })
        .catch(error => console.error("Error fetching order details:", error));
    },
    updateOrderStatus() {
      if (!this.newStatus) return;
      axios.post(`http://localhost:8000/api/shop/admin/orders/${this.selectedOrderId}/update_orderstatus/`, { status: this.newStatus })
        .then(() => {
          alert('Order status updated successfully');
          this.fetchOrders(); // Optionally refresh the list or the selected order
        })
        .catch(error => console.error("Error updating order status:", error));
    }
  }
}
</script>

<style scoped>
div {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

h2, h3 {
  color: #333;
}

select, button {
  width: 100%;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #f8f8f8;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  font-size: 16px;
}

button {
  cursor: pointer;
  background-color: #0056b3;
  color: white;
  border: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #007bff;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background-color: #fff;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

li span {
  display: block;
  margin-bottom: 5px;
}

.order-detail {
  font-size: 14px;
  color: #555;
}
</style>

