<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<template>
    <Navbar />
    <!-- Might need to be the username -->
     <h1>{{ $route.params.username }}</h1>
</template>