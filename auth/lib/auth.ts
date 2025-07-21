import {betterAuth} from "better-auth";
import {Pool} from "pg";
import {uploadImageToS3} from "./uploadToS3.ts";
import {callWebhook} from "./webhook.ts";
import {renderEmailTemplate, sendEmail} from "./emailSender.ts";
import {v4 as uuidv4} from 'uuid';
import config from '../config.ts';
import {getEnabledPlugins} from "./ee";

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
  plugins: getEnabledPlugins()
});