import {process} from "std-env";

export default defineNuxtRouteMiddleware(async (to) => {
  if (process.server) return

  // Public routes (excluding /login, which has special handling)
  const publicRoutes = ['/', '/about', '/contact', '/privacy', '/terms', '/cancellation', '/landing']
  if (publicRoutes.includes(to.path)) return

  if (to.query.redirect?.toString()) {
    return navigateTo(to.query.redirect?.toString())
  }
})