
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/HomePage.vue';
import ProductList from '../components/ViewProductList.vue';
import ProductDetail from '../components/ViewProductDetail.vue';
import UserRegister from '../components/UserRegister.vue';
import UserLogin from '../components/UserLogin.vue';
import PlaceOrder from '../components/PlaceOrder.vue';
import ViewOrders from '../components/OrderManagement.vue';
import AdminSupportTicketsManagement from '../components/AdminSupportTicketsManagement.vue';
import AdminTransactionsManagement from '../components/AdminTransactionsManagement.vue';
import AdminProductManagement from '../components/AdminProductManagement.vue'; 
import AdminOrderManagement from '../components/AdminOrderManagement.vue'; 
import AdminPage from '../components/AdminPage.vue'; 
import ViewTickets from '../components/SupportTicketsManagement.vue'; 

const routes = [
  // Customer side paths
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/products',
    name: 'ProductList',
    component: ProductList,
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: ProductDetail,
    props: true,
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister,
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/place_order',
    name: 'PlaceOrder',
    component: PlaceOrder,
    meta: { requiresAuth: true },
  },
  {
    path: '/my_orders',
    name: 'ViewOrders',
    component: ViewOrders,
    meta: { requiresAuth: true },
  },
  {
    path: '/my_tickets',
    name: 'ViewTickets',
    component: ViewTickets,
    meta: { requiresAuth: true },
  },
  {
    path: '/my_tickets/submit_ticket',
    name: 'SubmitTicket',
    component: ViewTickets,
    meta: { requiresAuth: true },
  },

  // Admin side paths
  {
    path: '/admin',
    name: 'AdminPage',
    component: AdminPage,
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/support_tickets',
    name: 'AdminSupportTicketsManagement',
    component: AdminSupportTicketsManagement,
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/transactions',
    name: 'AdminTransactionsManagement',
    component: AdminTransactionsManagement,
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/products',
    name: 'AdminProductManagement',
    component: AdminProductManagement,
    meta: { requiresAdmin: true },
  },
  {
    path: '/admin/orders',
    name: 'AdminOrderManagement',
    component: AdminOrderManagement,
    meta: { requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
