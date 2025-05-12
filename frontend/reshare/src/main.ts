import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura';
import { FormField } from '@primevue/forms';
import { Button, InputText, Message, Password, FloatLabel, Card, Divider, SplitButton, Textarea, InputNumber, InputIcon, IconField, Select, AutoComplete, Dialog } from 'primevue';

// for icons 
import 'primeicons/primeicons.css'
import { IcOrganicFood, BxBowlHot, FlFilledLeafTwo } from '@kalimahapps/vue-icons';

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
import CreateRecipe from './pages/CreateRecipe.vue'
import Profile from './pages/Profile.vue'
import Bookmarks from './pages/Bookmarks.vue'
import SearchPage from './pages/SearchPage.vue'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000';
// this will change the current page
const routes = [
    {path: '/', component: MainPage},
    {path: '/login', component: Login},
    {path: '/signup', component: Signup},
    {path: '/:username', children : [{path : 'homepage', component: Homepage}, {path : 'create', component : CreateRecipe}, 
                                     {path : 'profile', component: Profile}, {path : 'bookmarks', component: Bookmarks}, {path: 'search', component: SearchPage}] },
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
app.component('Textarea', Textarea)
app.component('InputNumber', InputNumber)
app.component('InputIcon', InputIcon)
app.component('IconField', IconField)
app.component('Select', Select)
app.component('AutoComplete', AutoComplete)
app.component('BxBowlHot', BxBowlHot);
app.component('Dialog', Dialog);
app.component('FlFilledLeafTwo', FlFilledLeafTwo);
app.mount('#app');
