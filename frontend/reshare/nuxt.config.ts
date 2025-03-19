import { defineNuxtConfig } from "nuxt/config";
import Aura from '@primeuix/themes/aura';
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  title : "Reshare",
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/image', '@primevue/nuxt-module'], 

  primevue: {
    options: {
      ripple : true,
      theme : {
        preset: Aura,
      }
    }
  }
})