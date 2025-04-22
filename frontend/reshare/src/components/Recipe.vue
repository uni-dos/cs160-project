<template>
    <Card style="width: max-content; overflow: hidden">
        <template #title>{{title}}</template>
        <template #subtitle> By {{ user }}  <p>{{ desc }}</p></template>
        <template #content>

            <p class="m-0">Servings {{ servings }}</p>
            <p class="m-0">
                {{ steps }}
            </p>

        </template>
        <template #footer>
            <div class="row">
                <Button severity="secondary" outlined class="w-full"> Sustainability: {{ rating }}</Button>
                <Button severity="info" outlined class="w-full" icon="pi pi-sparkles" label="Rate"></Button>
            </div>
        </template>
    </Card>
</template>

<script lang="ts">
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