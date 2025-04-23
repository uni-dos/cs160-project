import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura';
import { FormField } from '@primevue/forms';
import { Button, InputText, Message, Password, FloatLabel, Card, Divider, SplitButton} from 'primevue';

// for icons 
import 'primeicons/primeicons.css'
import { IcOrganicFood } from '@kalimahapps/vue-icons';

// custom component
import Navbar from './components/Navbar.vue';
import Recipe from './components/Recipe.vue';

import App from './App.vue'

import { createRouter, createWebHistory } from 'vue-router';

import Signup from './pages/Signup.vue';
import Login from './pages/Login.vue';
import MainPage from './pages/MainPage.vue'
import Homepage from './pages/Homepage.vue'
import axios from 'axios'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000';
// this will change the current page
const routes = [
    {path: '/', component: MainPage},
    {path: '/login', component: Login},
    {path: '/signup', component: Signup},
    {path: '/:username/homepage', component: Homepage},
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

const app = createApp(App);

app.use(router);

app.use(PrimeVue, {
    theme: {
        preset : Aura,
    }
});
app.component('FormField', FormField);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('Message', Message);
app.component('Password', Password);
app.component('FloatLabel', FloatLabel);
app.component('IcOrganicFood', IcOrganicFood);
app.component('Navbar', Navbar);
app.component('Card', Card);
app.component('Divider', Divider);
app.component('Recipe', Recipe);
app.component('SplitButton', SplitButton);
app.mount('#app');
