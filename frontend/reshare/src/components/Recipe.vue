<template>
    <Card style="width: max-content; overflow: hidden">
        <template #title>{{title}}</template>
        <template #subtitle>
        <div class="col">
            <Message variant="simple"> By {{ user }}</Message>
            <Message variant="simple" severity="secondary"> {{ desc }}</Message>
       
            <Message icon="pi pi-clock" variant="simple">{{ time }} </Message>
        
            <Message variant="simple"> <BxBowlHot/> Servings {{ servings }} </Message>

            <Message v-for="(i, index) in ingredients" :key="index"> {{ index + 1 }}: {{ i.amount }}{{ i.weight }} {{ i.ingredient_name }} </Message> 
            
        </div> 
      
        </template>
        <template #content>
            <Message variant="simple" severity="contrast">
                {{ steps }}
            </Message>

        </template>
        <template #footer>
            <div class="row">
                <Message severity="secondary" variant="outlined" class="w-full"> Sustainability: {{ rating }}</Message>
                <Button severity="info" outlined class="w-full" icon="pi pi-sparkles" label="Rate"></Button>
            </div>
        </template>
    </Card>
</template>

<script lang="ts">
import { type Ingredient } from '../data/Ingredient'
export default {
    props : {
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
    row-gap: 10px;
}
</style>