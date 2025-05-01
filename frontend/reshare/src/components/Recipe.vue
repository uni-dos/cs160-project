<template>
    <Card style="width: min-content; height: 490px; overflow: auto;">
        <template #title>{{title}}</template>
        <template #subtitle>
            <Divider />
        <div class="col">
            <Message variant="simple" severity="success"> By {{ user }}</Message>
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
                <Message severity="secondary" variant="outlined" class="w-full"> Sustainability: {{ rating }}</Message>
                <Button severity="info" class="w-full" icon="pi pi-sparkles" label="Rate" ></Button>
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
    row-gap: 12px;
}
</style>