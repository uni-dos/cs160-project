<template>
    <div class="header">
      <ul class="left-links">
        <Button @click="emitClicked('logo')"><IcOrganicFood/><label>Reshare</label></Button>
        <Button label="Following" icon="pi pi-users" @click="emitClicked('following')"></Button>
        <Button label="Bookmarks" icon="pi pi-bookmark" @click="emitClicked('bookmarks')"></Button>
        <Button label="Create" icon="pi pi-pen-to-square" @click="emitClicked('create')"></Button>
        <div class="search-container">
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="searchQuery" variant="filled" size="large" placeholder="Search" @keyup.enter="handleSearch" />
        </IconField>
        </div>
      </ul>
      <ul class="right-links">
        <SplitButton icon="pi pi-user" @click="emitClicked('profile')" :model="logout"><label>{{ $route.params.username }}</label></SplitButton>
        
      </ul>
    </div>
</template>

<script lang="ts">
import axios from 'axios'
export default {
  data () {
    return {
      searchQuery: '',
      logout : [{label : "Logout", command: async () => {
      await axios.post('/logout')
      .then (response => {
        if (response.status === 200) {
          this.$router.push('/');
        }
      })
      .catch(error => {
        console.log(error);
      });
      }}]}; 
  },
  methods: {
    emitClicked(buttonPressed : string) {
      if (buttonPressed === "create") {
        this.$router.push('create');
      } else if (buttonPressed === 'logo') {
        this.$router.push('homepage');
      }
    },
    handleSearch() {
      console.log("Searching for: ", this.searchQuery);
      this.searchQuery = '';
    }
  },
  props : {
    user : {
      type : String,
      default : "user"
    }
  }
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

.search-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-container input {
  padding: 8px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 200px; /* Adjust width as needed */
}


</style>