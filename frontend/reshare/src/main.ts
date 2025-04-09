import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura';
import { FormField } from '@primevue/forms';
import { Button, InputText, Message, Password } from 'primevue';
import App from './App.vue'

const app = createApp(App);


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


app.mount('#app');
