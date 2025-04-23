<template>
    <Navbar />
    <!-- Might need to be the username -->
     <h1>{{ $route.params.username }}</h1>

    <div class="row">
        <Recipe v-for="r in items" 
            :key="r.recipe_id" :title="r.title"
            :user="r.author_username" :steps="r.steps" :desc="r.short_description" 
            :rating="r.sustainability_rating" :servings="r.servings"/>
        
        </div>
</template>

<script lang="ts">
    import axios from 'axios'
    
    interface Recipe_Result {
        recipe_id : Number,
        title : String,
        short_description : String,
        steps : String,
        time : String,
        servings : Number,
        author_username : String,
        sustainability_rating : Number,
        average_rating : Number
    }
    export default {
        data () {
           return{ items : <Recipe_Result[]>[] }
        },
        async mounted() {
            await axios.get('/recipes')
            .then(response => {
                
                if (response.status === 200) {
                    // we got at least 1 post
                    console.log("Mounted")
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