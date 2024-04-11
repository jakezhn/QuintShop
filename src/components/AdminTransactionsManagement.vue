<template>
  <div class="transactions-container">
    <h2>All Transactions</h2>
    <ul class="transactions-list">
      <li v-for="transaction in transactions" :key="transaction.id" class="transaction-item">
        <span class="transaction-id">Transaction ID: {{ transaction.id }}</span>, 
        <span class="transaction-amount">Amount: ${{ transaction.amount }}</span>, 
        <span class="transaction-status">Status: {{ transaction.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      transactions: []
    };
  },
  mounted() {
    this.fetchTransactions();
  },
  methods: {
    fetchTransactions() {
      axios.get('http://localhost:8000/api/shop/transactions/')
        .then(response => (this.transactions = response.data))
        .catch(error => console.error("Error fetching transactions:", error));
    }
  }
}
</script>

<style scoped>
.transactions-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.transactions-list {
  list-style-type: none;
  padding: 0;
}

.transaction-item {
  background-color: #f9f9f9;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.transaction-id, .transaction-amount, .transaction-status {
  display: block;
}

.transaction-amount {
  color: #4CAF50; /* Green for amounts to make them stand out */
}

.transaction-status {
  font-weight: bold;
}
</style>
