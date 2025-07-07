import {createAuthClient} from "better-auth/client";
import {anonymous, bearer, jwt} from "better-auth/plugins"
import {organizationClient} from "better-auth/client/plugins"


export function useAuthClient() {
  const config = useRuntimeConfig()
  const {signIn, signUp, signOut, getSession, token, useListOrganizations, useActiveOrganization, organization} = createAuthClient({
    baseURL: config.public.authBaseUrl,
    advanced: {
      cookiePrefix: "rhobots"
    },
    plugins: [
      anonymous(),
      organizationClient(),
      jwt(),
      bearer({
        requireSignature: true
      })
    ]
  });

  const setJwtToken = async () => {
    const {data, error} = await token()
    if (error) throw error
    if (data?.token) {
      const userStore = useUserStore()
      userStore.setToken(data?.token)
    }
    return data?.token
  }

  return {
    signIn,
    signUp,
    signOut,
    getSession,
    setJwtToken,
    useListOrganizations,
    useActiveOrganization,
    organization
  }
}