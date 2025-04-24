<template>
    <div class="header">
      <ul class="left-links">
        <Button @click="emitClicked('logo')"><IcOrganicFood/><label>Rehare</label></Button>
        <Button label="Following" icon="pi pi-users" @click="emitClicked('following')"></Button>
        <Button label="Bookmarks" icon="pi pi-bookmark" @click="emitClicked('bookmarks')"></Button>
        <Button label="Create" icon="pi pi-pen-to-square" @click="emitClicked('create')"></Button>
      </ul>
      <ul class="right-links">
        <SplitButton label="Profile" icon="pi pi-user" @click="emitClicked('profile')" :model="logout"></SplitButton>
        
      </ul>
    </div>
</template>

<script lang="ts">
import axios from 'axios'
export default {
  data () {
    return {logout : [{label : "Logout", command: async () => {
      await axios.post('/logout')
      .then (response => {
        if (response.status === 200) {
          this.$router.push('/');
        }
      })
      .catch(error => {
        console.log(error);
      });
      console.log("Logout")}}]}; 
  },
  methods: {
    emitClicked(buttonPressed : string) {
      if (buttonPressed === "create") {
        this.$router.push('create');
      } else if (buttonPressed === 'logo') {
        this.$router.push('homepage');
      }
    },
  },
};
</script>

<style scoped>

.header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 16px;
}


</style>