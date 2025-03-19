import { defineNuxtConfig } from "nuxt/config";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  title : "Reshare",
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/image', '@primevue/nuxt-module']
})