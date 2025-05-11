<template>
    <Navbar />

    <h2>@{{ $route.params.username }}</h2>
    <h3>Recipes:</h3>
    <div class="row">
        <Recipe v-for="r in items" 
            :key="r.recipe_id" :title="r.title" :recipeId="r.recipe_id"
            :user="r.author_username" :steps="r.steps" :desc="r.short_description" 
            :rating="r.sustainability_rating" :servings="r.servings" :time="r.time" :average_rating="r.average_rating" :ingredients="r.ingredients"/>
    </div>
</template>
<script lang="ts">
    import axios from 'axios'
    import { type Recipe_Result } from '../data/Ingredient'
    export default {
        data () {
            return {
                items : <Recipe_Result[]>[] 
            }
        },
        methods: {
            async fetchUserData() {
                await axios.get(`/user/${this.$route.params.username}`)
                .then(response => {
                    if (response.status === 200) {
                        this.items = response.data.recipes;
                    }
                    else {
                        this.items = [];
                    }
                })
                .catch(error => {
                    console.log(error);
                    this.$router.push('/login');
                })
            }
        },
        mounted() {
            this.fetchUserData();
        }
    }
</script>

<style scoped>
.row {
    display: flex;
    grid-auto-flow: row;
    gap: 10px;
}
</style>