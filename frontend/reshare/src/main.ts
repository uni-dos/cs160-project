import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura';
import { FormField } from '@primevue/forms';
import { Button, InputText, Message, Password, FloatLabel, Card, Divider, ProgressSpinner, Textarea, InputNumber, InputIcon, IconField, Select } from 'primevue';

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
import CreateRecipe from './pages/CreateRecipe.vue'

// this will change the current page
const routes = [
    {path: '/', component: MainPage},
    {path: '/login', component: Login},
    {path: '/signup', component: Signup},
    {path: '/:username/homepage', component: Homepage},
    {path: '/:username/create', component: CreateRecipe}
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
app.component('ProgressSpinner', ProgressSpinner);
app.component('Textarea', Textarea)
app.component('InputNumber', InputNumber)
app.component('InputIcon', InputIcon)
app.component('IconField', IconField)
app.component('Select', Select)
app.mount('#app');
