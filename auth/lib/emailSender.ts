import pkg from "@aws-sdk/client-sesv2";
import config from '../config.ts';
import path from 'path';
import {promises as fs} from 'fs';

const {SESv2Client, SendEmailCommand} = pkg

// Create SES service object
const sesClient = new SESv2Client({
  region: config.AWS_REGION,
  credentials: {
    accessKeyId: config.AWS_ACCESS_KEY_ID,
    secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
  },
});

interface EmailParams {
  to: string[];
  subject: string;
  body: string;
  isHtml?: boolean;
}

export async function sendEmail(params: EmailParams): Promise<string> {
  if (!config.AWS_SENDER_EMAIL) {
    return 'AWS_SENDER_EMAIL not configured'
  }

  const {to, subject, body, isHtml = false} = params;
  const sendEmailParams = {
    FromEmailAddress: config.AWS_SENDER_EMAIL,
    Destination: {
      ToAddresses: to
    },
    Content: {
      Simple: {
        Body: {
          [isHtml ? "Html" : "Text"]: {
            Charset: "UTF-8",
            Data: body,
          },
        },
        Subject: {
          Charset: "UTF-8",
          Data: subject,
        }
      }
    },
    ListManagementOptions: {
      ContactListName: 'General',
      TopicName: 'Account'
    }
  };


  try {
    const command = new SendEmailCommand(sendEmailParams);
    const response = await sesClient.send(command);
    return response.MessageId || "No message ID returned";
  } catch (err) {
    console.error("Error sending email:", err);
    throw err;
  }
}

export async function renderEmailTemplate(templateName: string, variables: any) {
  const templatePath = path.join('email_templates', `${templateName}.html`);
  let template = await fs.readFile(templatePath, 'utf-8');

  const currentYear: number = new Date().getFullYear();
  const finalVariables = {
    ...variables, currentYear
  }

  // Replace all placeholders with actual values
  Object.keys(finalVariables).forEach(key => {
    template = template.replace(new RegExp(`{{${key}}}`, 'g'), finalVariables[key]);
  });

  return template;
}

// Example usage
// (async () => {
//   const body = await renderEmailTemplate('reset_password', {
//     username: 'Ravi',
//     verificationLink: 'https://abcd.com'
//   })
//   try {
//     const messageId = await sendEmail({
//       to: ['ravipiplani@outlook.com'],
//       subject: "Reset your password",
//       body: body,
//       isHtml: true
//     });
//     console.log(`Email sent with message ID: ${messageId}`);
//   } catch (error) {
//     console.error("Failed to send email:", error);
//   }
// })();