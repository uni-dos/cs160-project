<template>
  <div class="container">
    <form @submit.prevent="handleSubmit" class="centered">
      <FormField label="Username">
        <InputText v-model="username" id="username" placeholder="Username" required />
      </FormField>

      <FormField label="Password">
        <Password v-model="password" id="password" placeholder="Password" required />
      </FormField>

      <Button label="Sign Up" type="submit" :disabled="isSubmitting" />
    </form>

    <div v-if="errorMessage">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      isSubmitting: false,
      errorMessage: ''
    };
  },
  methods: {
    async handleSubmit() {
      // The fields can never be empty as primvue checks
       await axios.post('http://localhost:5000/signup', {
          username: this.username,
          password : this.password
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });


      
    }
  }
};
</script>

<style scoped>

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.centered {
  display: flex;
  flex-direction: column;   
  gap: 10px;
  text-align: center;   
}


</style>
