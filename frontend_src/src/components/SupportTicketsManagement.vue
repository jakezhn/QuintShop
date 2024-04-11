<template>
  <div class="container">
    <form @submit.prevent="submitTicket" class="ticket-form">
      <h2>Submit Support Ticket</h2>
      <input v-model="subject" placeholder="Subject" class="input-field">
      <textarea v-model="description" placeholder="Description" class="textarea-field"></textarea>
      <button type="submit" class="submit-btn">Submit Ticket</button>
    </form>

    <div class="tickets">
      <h2>My Tickets</h2>
      <div v-for="ticket in tickets" :key="ticket.id" class="ticket">
        <h3>{{ ticket.subject }}</h3>
        <p>{{ ticket.description }}</p>
        <p>Status: {{ ticket.status }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      subject: '',
      description: '',
      tickets: []
    };
  },
  mounted() {
    this.fetchTickets();
  },
  methods: {
    submitTicket() {
      const data = {
        subject: this.subject,
        description: this.description
      };
      axios.post('http://localhost:8000/api/shop/my_tickets/submit_ticket/', data)
        .then(() => {
          alert('Ticket submitted successfully');
          this.subject = '';
          this.description = '';
          this.fetchTickets(); // Refresh the list of tickets
        })
        .catch(error => {
          console.error("Error submitting ticket:", error);
        });
    },
    fetchTickets() {
      axios.get('http://localhost:8000/api/shop/my_tickets/')
        .then(response => {
          this.tickets = response.data;
        })
        .catch(error => {
          console.error("Error fetching tickets:", error);
        });
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.ticket-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.input-field, .textarea-field {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 16px;
}

.textarea-field {
  resize: vertical;
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

.tickets {
  margin-top: 20px;
}

.ticket {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
