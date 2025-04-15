<script setup>
</script>

<template>
    <div class="header">
      <ul class="left-links">
        <li><a href="#">Reshare</a></li>
        <li><a href="#">Following</a></li>
        <li><a href="#">Bookmarks</a></li>
        <li><a href="#">Create</a></li>
      </ul>
      <ul class="right-links">
        <li><a href="#">Profile</a></li>
      </ul>
    </div>
</template>

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

a {
  color: white;
  text-decoration: none;
}

</style>