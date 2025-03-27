<script setup lang="ts">
import { NuxtLink } from '#components';

</script>


<template>
  <Toolbar>
    <template #start>
      <NuxtLink to="/">
        <Button label="Reshare"/>
      </NuxtLink>
      
    </template>


    <template #end>

      <div class="flex flex-row gap-1">
      
          <NuxtLink to="login"> 
            <Button label="Login" />
          </NuxtLink>
       
        <Button label="Signup"/>
      </div>

    </template>
  </Toolbar>
  <div>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  </div>
</template>



