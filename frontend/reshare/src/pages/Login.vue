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
          <Password v-model="password" id="password" :feedback="false" toggleMask required />
          <label for="password">Password</label>
          </FormField>
        </FloatLabel>
  
        <Button label="Log In" type="submit" :disabled="isSubmitting" />
      </form>
  
      <div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
        await axios.post('/login', {
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
            // retrieve the "taken" or "message field from backend response"
            if (error.response && error.response.data && error.response.data.message) {
              this.errorMessage = error.response.data.message;
            }
            else {
              this.errorMessage = "Could not login. Try again later";
            }
          });
          this.isSubmitting = false;
          
        
      }
    }
  };
  </script>
  
  <style scoped>
  
  .container {
    display: flex;
    flex-direction: column;
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

  .error {
    color: red;
  }
  
  
  </style>
  