import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

axios.defaults.withCredentials = true 
// CORS (Cross-Origin Resource Sharing, Vue and Django in different domains)
// caused Axios can not send cookie by default (in protection for Cross Site Scripting Attack)
// https://stackoverflow.com/questions/42221377/vue-or-axios-dont-store-session-cookie

const app = createApp(App);
app.use(router);
app.mount('#app');
