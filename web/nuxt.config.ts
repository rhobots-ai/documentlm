// https://nuxt.com/docs/api/configuration/nuxt-config
import {process} from "std-env";

export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  // nitro: {
  //   static: true,
  //   prerender: {
  //     failOnError: false,
  //   }
  // },
  devtools: {enabled: false},
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    'nuxt-gtag',
    '@nuxtjs/google-fonts'
  ],
  gtag: {
    enabled: process.env.NODE_ENV === 'production',
    id: process.env.NUXT_PUBLIC_GOOGLE_ANALYTICS_ID
  },
  googleFonts: {
    families: {
      Roboto: true
    },
    display: 'swap',
    preload: true,
    preconnect: true,
  },
  css: ['~/assets/css/main.css'],
  app: {
    pageTransition: {name: 'page', mode: 'out-in'}
  },
  runtimeConfig: {
    public: {
      appBaseUrl: process.env.NUXT_PUBLIC_APP_BASE_URL,
      apiScheme: process.env.NUXT_PUBLIC_API_SCHEME,
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL,
      s3Url: process.env.NUXT_PUBLIC_S3_URL,
      authBaseUrl: process.env.NUXT_PUBLIC_AUTH_BASE_URL,
    },
  }
})