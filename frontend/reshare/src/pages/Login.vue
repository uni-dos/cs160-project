<template>
    <div class="container">
      <form @submit.prevent="handleSubmit" class="centered">
        <FloatLabel variant="on">
            <FormField label="Username">
            <InputText v-model="username" id="username" required variant="filled" size="large"/>
            <label for="username">Username</label>
        </FormField>
        </FloatLabel>
  
        <FloatLabel variant="on">
          <FormField label="Password">
          <Password v-model="password" id="password" toggleMask required />
          <label for="password">Password</label>
          </FormField>
        </FloatLabel>
  
        <Button label="Log In" type="submit" :disabled="isSubmitting" />
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
        this.isSubmitting = true;
        
        // The fields can never be empty as primvue checks
        await axios.post('http://localhost:5000/login', {
            "username": this.username,
            "password" : this.password
          })
          .then(response => {
            console.log(response);
            // pass in username
            // so router.push(nextpage params: username)
            if (response.status === 201) {
              // move to the next page
              this.$router.push('/' + response.data.username + '/homepage');
            }
          })
          .catch(error => {
            // error.response.data
            console.log(error.response.data.message);
          });
          this.isSubmitting = false;
          
        
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
  