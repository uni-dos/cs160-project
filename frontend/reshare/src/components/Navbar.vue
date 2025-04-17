<template>
    <div class="header">
      <ul class="left-links">
        <Button><IcOrganicFood/><label>Rehare</label></Button>
        <Button label="Following" icon="pi 
pi-users" @click="emitClicked('following')"></Button>
        <Button label="Bookmarks" icon="pi pi-bookmark" @click="emitClicked('bookmarks')"></Button>
        <Button label="Create" icon="pi pi-pen-to-square" @click="emitClicked('create')"></Button>
      </ul>
      <ul class="right-links">
        <Button label="Profile" icon="pi pi-user" @click="emitClicked('profile')"></Button>
      </ul>
    </div>
</template>

<script lang="ts">

export default {
  methods: {
    emitClicked(buttonPressed : string) {
      console.log(buttonPressed);
      this.$emit(buttonPressed);
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