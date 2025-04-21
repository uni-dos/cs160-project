<template>
    <Card style="width: 25rem; overflow: hidden">
        
        <template #title>{{title}}</template>
        <template #subtitle>{{ desc }}</template>
        <template #content>
            <p class="m-0">
                {{ steps }}
            </p>
        </template>
        <template #footer>
            <div class="flex gap-4 mt-1">
                <Button label="Cancel" severity="secondary" outlined class="w-full" />
                <Button label="Save" class="w-full" />
            </div>
        </template>
    </Card>
</template>

<script lang="ts">
export default {
    props : {
        title : {
            type : String
        },
        desc : {
            type : String
        },
        steps : {
            type : String
        },
    }
}
</script>


