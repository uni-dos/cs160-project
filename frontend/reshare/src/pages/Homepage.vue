<template>
    <Navbar />
    <!-- Might need to be the username -->
     <h1>{{ $route.params.username }}</h1>

</template>

<script lang="ts">
    import axios from 'axios'
    export default {
        async mounted() {
            await axios.get('http://localhost:5000/posts')
            .then(response => {
                if (response.status === 201) {
                    // we got at least 1 post
                }
                else if (response.status === 303) {
                    // no posts
                }
            })
            .catch(error => {

            });
        },
    }

</script>