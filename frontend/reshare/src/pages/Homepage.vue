<template>
    <Navbar />

    <div class="row">
        <Recipe v-for="r in items" 
            :key="r.recipe_id" class="recipe-card" :title="r.title" :recipeId="r.recipe_id"
            :user="r.author_username" :steps="r.steps" :desc="r.short_description" 
            :rating="r.sustainability_rating" :servings="r.servings" :time="r.time" :average_rating="r.average_rating" :ingredients="r.ingredients"/>
        
        </div>
</template>

<script lang="ts">
    import axios from 'axios'
    import { type Recipe_Result } from '../data/Ingredient'
    
    export default {
        data () {
           return{ items : <Recipe_Result[]>[] }
        },
        async mounted() {
            await axios.get('/recipes')
            .then(response => {
                
                if (response.status === 200) {
                    // we got at least 1 post
                    console.log("Mounted");
                    this.items = response.data;
                }
                else if (response.status === 303) {
                    // no posts
                }
            })
            .catch(error => {
                console.log(error);
                this.$router.push('/login');
            });
        },
    }

</script>

<style scoped>
.row {
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: center;
    gap: 20px;
}

.recipe-card {
    flex: 1 1 300px;
    max-width: 300px;
    min-width: 250px;
    overflow: hidden;
    scrollbar-width: none;
    outline: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 8px;
    padding: 5px;
}
</style>