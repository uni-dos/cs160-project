<template>
    <div class="signup-container">
      <h1>Sign Up</h1>
      <form submit="handleSubmit">
        <div>
          <label for="username">Username:</label>
          <input type="username" id="username" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Sign Up</button>
      </form>
  
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success">{{ successMessage }}</div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import axios from 'axios'
  
  export default defineComponent({
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
        successMessage: '',
      };
    },
    methods: {
      async handleSubmit() {
        try {
          const response = await axios.post('http://localhost:5000/signup', {
            username: this.username,
            password: this.password,
          });
  
          if (response.status === 201) {
            this.successMessage = response.data.message;
            this.errorMessage = '';
          }
        } catch (error: any) {
          this.errorMessage = error.response.data.message;
          this.successMessage = '';
        }
      },
    },
  });
  </script>