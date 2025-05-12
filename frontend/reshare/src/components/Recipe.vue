<template>
    <Card style="width: min-content; height: 490px; overflow: auto;">
        <template #title>{{title}}</template>
        <template #subtitle>
            <Divider />
        <div class="col">
            <Message variant="simple" severity="success">
                Created by <router-link :to="`/${user}/profile`" class="profile-link">@{{ user }}</router-link>
            </Message>
            <Message variant="simple" severity="secondary"> {{ desc }}</Message>
       
            <Message icon="pi pi-clock" variant="simple">{{ time }} </Message>
        
            <Message variant="simple"> <BxBowlHot/> Servings {{ servings }} </Message>
            <Divider />
            <Message severity="warn" variant="simple" size="large">Ingredients:</Message>
            <Message v-for="(i, index) in ingredients" :key="index" severity="contrast" variant="simple"> {{ index + 1 }}: {{ i.amount }} {{ i.weight }} {{ i.ingredient_name }} </Message> 
            
        </div>  
      
        </template>
        <template #content>
            <Divider/>
            <div class="col">
                <Message variant="simple" severity="warn" size="large">Steps:</Message>
            
                <Message variant="simple" severity="contrast" v-for="(i, index) in steps.split('<br>')">
                {{ index + 1 }}. {{ i }}
            </Message>
            </div>

            <Divider />
        </template>
       
        <template #footer>
            <div class="row">
                <Message severity="success" variant="outlined" class="w-full"> <FlFilledLeafTwo/> {{ rating }} kgCO&#8322;e</Message>
                <Button
                    :icon="Array.from(bookmarkedRecipes).includes(recipeId) ? 'pi pi-bookmark-fill' : 'pi pi-bookmark'"
                    severity="secondary"
                    class="w-full"
                    @click="toggleBookmark(recipeId)"
                ></Button>
            </div>
        </template>
    </Card>
</template>

<script lang="ts">
import axios from 'axios'
import { type Ingredient } from '../data/Ingredient'
import { FlFilledLeafTwo, IcOrganicFood, IcOrganicFoodSquare } from '@kalimahapps/vue-icons';
export default {
    props : {
        recipeId: {
            type: Number,
            required: true
        },
        user : {
            type : String,
            default : "user"
        },
        title : {
            type : String,
            default : "Title"
        },
        desc : {
            type : String,
             default : "Desc"
        },
        steps : {
            type : String,
             default : "Steps"
        },
        rating : {
            type : Number,
            default: 10
        },
        servings : {
            type : Number,
            default: 2
        },
        time : {
            type : String,
            default : ""
        },
        ingredients : {
            type : Array<Ingredient>,
        }
    },
    data() {
        return {
            bookmarkedRecipes: [] as Number[],
            sessionUsername: ''
        };
    },
    mounted() {
        this.fetchSessionUsername();
    },
    methods: {
        async fetchBookmarkedRecipes() {
            await axios.get(`/get-bookmarks-by-id/${this.sessionUsername}`)
                    .then(response => {
                        if (response.status === 200) {
                            console.log(this.bookmarkedRecipes)
                            this.bookmarkedRecipes = response.data.bookmarks;
                        }
                    })
                    .catch(error => {
                        console.log(error);
                        // this.$router.push('/login');
                    })
        },
        async toggleBookmark(recipeId : Number) {
            const isBookmarked = this.bookmarkedRecipes.includes(recipeId);
            try {
                if (isBookmarked) {
                    await axios.delete(`/bookmark/${this.sessionUsername}/${recipeId}`);
                    this.bookmarkedRecipes = this.bookmarkedRecipes.filter(id => id !== recipeId);
                } else {
                    await axios.post(`/bookmark/${this.sessionUsername}/${recipeId}`);
                    this.bookmarkedRecipes = [...this.bookmarkedRecipes, recipeId];
                }
            } catch (error) {
                console.error('Error toggling bookmark:', error);
            }
        },
        async fetchSessionUsername() {
            try {
                const response = await axios.get('/session-username')
                if (response.status === 200) {
                this.sessionUsername = response.data.username;
                this.fetchBookmarkedRecipes();
                }
                else {
                console.log(response.data.message);
                }
            } catch (error) {
                this.$router.push('/');
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
.col {
    display: flex;
    flex-direction: column;
    row-gap: 12px;
}
.profile-link {
    text-decoration: none;
    color: inherit;
    font-weight: bold;
}
.profile-link:hover {
    text-decoration: underline;
}
</style>