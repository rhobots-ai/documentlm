import axios from 'axios';
import crypto from 'crypto';
import config from '../config.ts';

const {AxiosResponse, AxiosError} = axios;

interface WebhookPayload {
  type?: string
  data?: {
    [key: string]: any;
  }
}

interface WebhookResponse {
  status: string;

  [key: string]: any; // Flexible response structure
}

/**
 * Generates HMAC SHA256 signature for webhook payload
 * @param payload - The data to be sent to the webhook
 * @param secret - Shared secret key for signing
 * @returns Hexadecimal string signature
 */
export function generateSignature(payload: WebhookPayload, secret: string): string {
  const secretBytes = Buffer.from(secret, 'utf8');
  const payloadBytes = Buffer.from(JSON.stringify(payload));
  return crypto
    .createHmac('sha256', secretBytes)
    .update(payloadBytes)
    .digest('hex');
}

/**
 * Calls the Django webhook endpoint with signed payload
 * @param payload - Data to send to the webhook
 * @returns Promise with the webhook response
 */
export async function callWebhook(
  payload: WebhookPayload
): Promise<WebhookResponse> {
  try {
    const secret = config.WEBHOOK_SECRET
    const signature = generateSignature(payload, secret)
    const response: AxiosResponse<WebhookResponse> = await axios.post(
      config.WEBHOOK_EP,
      payload,
      {
        headers: {
          'X-Signature': signature,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      // The request was made and the server responded with a status code
      throw new Error(`Webhook call failed with status ${axiosError.response.status}: ${JSON.stringify(axiosError.response.data)}`);
    } else if (axiosError.request) {
      // The request was made but no response was received
      throw new Error('No response received from webhook server');
    } else {
      // Something happened in setting up the request
      throw new Error(`Error setting up webhook request: ${axiosError.message}`);
    }
  }
}