<template>
  <div>
    <h2>Update Support Tickets</h2>
    <ul>
      <li v-for="ticket in tickets" :key="ticket.id">
        <p>{{ ticket.subject }} - {{ ticket.description }} - Status: {{ ticket.status }}</p>
        <select v-model="ticket.newStatus" @change="updateTicketStatus(ticket.id, ticket.newStatus)">
          <option v-for="statusOption in statusOptions" :key="statusOption" :value="statusOption">
            {{ statusOption }}
          </option>
        </select>
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
