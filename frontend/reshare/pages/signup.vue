<template>
  <form @submit.prevent="handleSingUp" class="flex flex-col gap-4 w-full sm:w-56">
   
    <div class="flex flex-col gap-1">
      
      <InputText
        id="username"
        v-model="username"
        placeholder="Username"
      />
      
    </div>

    <div class="flex flex-col gap-1">
      
      <Password
        id="password"
        v-model="password"
        feedback="false"
        placeholder="Password"
        
      />
    </div>

    <Button label="SignUp" type="submit"/>
  </form>

</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const username = ref('');
const password = ref('');

const handleSingUp = async () => {
  // send a request
  if (username.value && password.value) {
      const response = await axios.post('http://localhost:5000/signup', {
        username: this.username.value,
        password: this.password.value,
      });

      if (response.status === 201) {
        // created account now go to login page
      }
      // anything else get the error
      // and say what the issue was
  }
};
</script>