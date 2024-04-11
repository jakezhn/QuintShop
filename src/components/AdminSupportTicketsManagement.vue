<template>
  <div class="tickets-container">
    <h2>Update Support Tickets</h2>
    <ul class="ticket-list">
      <li v-for="ticket in tickets" :key="ticket.id" class="ticket-item">
        <div class="ticket-details">
          <p>{{ ticket.subject }} - {{ ticket.description }} - Status: {{ ticket.status }}</p>
          <select v-model="ticket.newStatus" @change="updateTicketStatus(ticket.id, ticket.newStatus)" class="status-dropdown">
            <option disabled value="">Change Status</option>
            <option v-for="statusOption in statusOptions" :key="statusOption" :value="statusOption">
              {{ statusOption }}
            </option>
          </select>
        </div>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios';

export default {
data() {
  return {
    tickets: [],
    statusOptions: ['Open', 'In Progress', 'Resolved', 'Closed'],
  };
},
mounted() {
  this.fetchOpenSupportTickets();
},
methods: {
  fetchOpenSupportTickets() {
    axios.get('http://localhost:8000/api/shop/admin/support_tickets/')
      .then(response => {
        this.tickets = response.data.map(ticket => ({
          ...ticket,
          newStatus: ticket.status // Initialize newStatus with the current status
        }));
      })
      .catch(error => console.error("Error fetching open support tickets:", error));
  },
  updateTicketStatus(ticketId, newStatus) {
    axios.post(`http://localhost:8000/api/shop/admin/support_tickets/${ticketId}/update_ticket/`, { status: newStatus })
      .then(() => {
        alert('Ticket status updated successfully');
        this.fetchOpenSupportTickets(); // Refresh tickets to reflect the updated status
      })
      .catch(error => {
        console.error("Error updating ticket status:", error);
        alert('Failed to update ticket status');
      });
  }
}
}
</script>

<style scoped>
.tickets-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: #f8f8f9;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  text-align: center;
}

.ticket-list {
  list-style: none;
  padding: 0;
}

.ticket-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 15px;
  margin-top: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ticket-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ticket-details p {
  margin: 0;
  color: #555;
  flex-grow: 1;
}

.status-dropdown {
  margin-left: 10px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: white;
}

.status-dropdown:hover {
  border-color: #888;
}

@media (max-width: 600px) {
  .ticket-details {
    flex-direction: column;
  }

  .status-dropdown {
    width: 100%;
    margin-top: 10px;
  }
}
</style>
