<template>
    <Navbar />

    <h2>Search Results for "{{ searchQuery }}"</h2>

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
            return {
                searchQuery: '', 
                items : <Recipe_Result[]>[] 
            }
        },
        methods: {
            async fetchSearchResults(query: string) {
                if (query) {
                    await axios.get(`/search/${query}`)
                    .then(response => {
                        if (response.status === 200) {
                            this.items = response.data.search_results;
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
            }
        },
        watch: {
            '$route.query.q': {
                immediate: true,
                handler(newQuery) {
                    if (newQuery) {
                        this.searchQuery = decodeURI(newQuery);
                        this.fetchSearchResults(this.searchQuery);
                    }
                }

            }
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