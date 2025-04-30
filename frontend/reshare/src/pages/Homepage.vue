<template>
    <Navbar />

    <div class="row">
        <Recipe v-for="r in items" 
            :key="r.recipe_id" :title="r.title"
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
    grid-auto-flow: row;
    gap: 10px;
}
</style>