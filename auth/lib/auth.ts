import {betterAuth} from "better-auth";
import {Pool} from "pg";
import {admin, anonymous, bearer, haveIBeenPwned, jwt, openAPI, organization} from "better-auth/plugins"
import {uploadImageToS3} from "./uploadToS3.ts";
import {callWebhook} from "./webhook.ts";
import {renderEmailTemplate, sendEmail} from "./emailSender.ts";
import {v4 as uuidv4} from 'uuid';
import config from '../config.ts';
import {createAuthMiddleware} from "better-auth/api";
import psl from 'psl';

function getTopLevelDomain(hostname: string): string {
  const parsed: any = psl.parse(hostname);
  return parsed.domain || hostname;
}

function updateCookieDomain(cookie: string, newDomain: string) {
  return cookie
    .replace(
      /Domain=\.[a-zA-Z0-9.-]+/g,
      `Domain=.${newDomain}` // Ensures new domain starts with a dot
    )
}

const hook = createAuthMiddleware(async (ctx) => {
  if (ctx.path === '/callback/:id' || ctx.path === 'get-session') {
    const origin = ctx.context.responseHeaders?.get('location')
    if (!origin) {
      return
    }
    const url = new URL(origin);
    const cookieDomain = getTopLevelDomain(url.hostname)
    if (ctx.context.responseHeaders?.get('set-cookie')) {
      let cookie = ctx.context.responseHeaders?.get('Set-Cookie');

      if (!cookie) return

      // Modify domain for each cookie
      const updatedCookie = updateCookieDomain(cookie, cookieDomain);

      ctx.context.responseHeaders?.set('Set-Cookie', updatedCookie);
    }
  }
  // return ctx.json()
});

export const auth = betterAuth({
  trustedOrigins: config.TRUSTED_ORIGINS,
  database: new Pool({
    connectionString: config.DATABASE_STRING,
  }),
  hooks: {
    // after: hook
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60 // Cache duration in seconds
    }
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: config.REQUIRE_EMAIL_VERIFICATION,
    sendResetPassword: async ({user, url, token}, request) => {
      try {
        const body = await renderEmailTemplate('reset_password', {
          username: user.name,
          resetPasswordLink: url
        })
        const messageId = await sendEmail({
          to: [user.email],
          subject: "Reset your password",
          body: body,
          isHtml: true
        });
        console.log(`Email sent with message ID: ${messageId}`);
      } catch (error) {
        console.error("Failed to send email:", error);
      }
    },
  },
  emailVerification: {
    sendVerificationEmail: async ({user, url, token}, request) => {
      const body = await renderEmailTemplate('verify_email', {
        username: user.name,
        verificationLink: url
      })
      try {
        const messageId = await sendEmail({
          to: [user.email],
          subject: "Verify your email address",
          body: body,
          isHtml: true
        });
        console.log(`Email sent with message ID: ${messageId}`);
      } catch (error) {
        console.error("Failed to send email:", error);
      }
    },
    sendOnSignUp: true,
    autoSignInAfterVerification: true,
    expiresIn: 3600
  },
  databaseHooks: {
    user: {
      create: {
        before: async (user) => {
          // upload image to s3 and save url
          let imageUrl = null
          if (user.image) {
            const uniqueId: string = uuidv4();
            imageUrl = await uploadImageToS3(user.image, config.AWS_STORAGE_BUCKET_NAME, `profile-pictures/${uniqueId}.jpg`)
          }
          return {data: {...user, image: imageUrl}};
        },
        after: async (user) => {
          const nameSplit = user.name.split(' ')
          await callWebhook({
            type: 'user.created',
            'data': {
              id: user.id,
              first_name: nameSplit[0],
              last_name: nameSplit.length > 1 ? nameSplit[nameSplit.length - 1] : null,
              email: user.email,
              image: user.image,
            }
          })
        }
      }
    }
  },
  socialProviders: {
    github: {
      prompt: "select_account",
      clientId: config.GITHUB_CLIENT_ID,
      clientSecret: config.GITHUB_CLIENT_SECRET,
    },
    google: {
      prompt: "select_account",
      clientId: config.GOOGLE_CLIENT_ID,
      clientSecret: config.GOOGLE_CLIENT_SECRET,
    },
    microsoft: {
      requireSelectAccount: true,
      clientId: config.MICROSOFT_CLIENT_ID,
      clientSecret: config.MICROSOFT_CLIENT_SECRET,
    }
  },
  advanced: {
    cookiePrefix: "rhobots",
    crossSubDomainCookies: {
      enabled: true,
      domain: `.${config.BASE_DOMAIN}`
    },
    defaultCookieAttributes: {
      secure: true,
      httpOnly: true,
      sameSite: "none"
    }
  },
  plugins: [
    anonymous(),
    haveIBeenPwned({
      customPasswordCompromisedMessage: 'Password has been found in an online data breach. For account safety, please use a different password.'
    }),
    admin(),
    organization({
      organizationLimit: 1,
      membershipLimit: 1,
      invitationLimit: 10000,
      organizationCreation: {
        afterCreate: async ({ organization, member, user }, request) => {
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
    }),
    openAPI(),
    jwt(),
    bearer({
      requireSignature: true
    })
  ]
});