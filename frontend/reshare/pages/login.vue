<template>
  <div>
    <Button label="Login" />

    <Form :zodResolver="zodResolver" @submit="onFormSubmit" class="flex flex-col gap-4 w-full sm:w-56">
      <FormField v-slot="$field" name="username" initialValue="" class="flex flex-col gap-1">
        <InputText v-model="$field.value" type="text" placeholder="Username" />
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>
      <Button type="submit" severity="secondary" label="Submit" />
    </Form>
  </div>
</template>

<script lang="ts" setup>
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { FormField, Form } from '@primevue/forms';



const onFormSubmit = (values: any) => {
  
  console.log(values.values.username);
};
</script>

<style>
/* Add your styles here */
</style>