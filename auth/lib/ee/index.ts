import {admin, anonymous, bearer, haveIBeenPwned, jwt, openAPI, organization} from "better-auth/plugins";
import {callWebhook} from "../webhook.ts";
import {isEeAvailable} from "./licensing/verify.ts";
import {BetterAuthPlugin} from "better-auth";

export function getEnabledPlugins(): BetterAuthPlugin[] {
  const plugins: BetterAuthPlugin[] = [
    anonymous(),
    haveIBeenPwned({
      customPasswordCompromisedMessage: 'Password has been found in an online data breach. For account safety, please use a different password.'
    }),
    admin(),
    openAPI(),
    jwt(),
    bearer({
      requireSignature: true
    })
  ]

  if (isEeAvailable()) {
    plugins.push(organization({
      organizationLimit: 1,
      membershipLimit: 1,
      invitationLimit: 10000,
      organizationCreation: {
        afterCreate: async ({organization, member, user}, request) => {
          await callWebhook({
            type: 'organization.created',
            'data': {
              id: organization.id,
              name: organization.name,
              slug: organization.slug,
              metadata: organization.metadata,
              created_by_id: user.id
            }
          })
        }
      }
    }))
  }

  return plugins
}