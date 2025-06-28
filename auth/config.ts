interface AppConfig {
  NODE_ENV: 'development' | 'production' | 'test';
  PORT: number;
  BASE_DOMAIN: string;
  BETTER_AUTH_SECRET: string;
  BETTER_AUTH_URL: string;
  TRUSTED_ORIGINS: string[];
  DATABASE_STRING: string;

  GOOGLE_CLIENT_ID: string;
  GOOGLE_CLIENT_SECRET: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  MICROSOFT_CLIENT_ID: string;
  MICROSOFT_CLIENT_SECRET: string;

  AWS_ACCESS_KEY_ID: string;
  AWS_SECRET_ACCESS_KEY: string;
  AWS_REGION: string;
  AWS_S3_BUCKET: string;
  AWS_SENDER_EMAIL: string;

  WEBHOOK_SECRET: string;
  WEBHOOK_EP: string;
}

const getConfig = (): AppConfig => {
  return {
    NODE_ENV: process.env.NODE_ENV as 'development' | 'production' | 'test' || 'development',
    PORT: Number(process.env.PORT) || 10000,
    BASE_DOMAIN: process.env.BASE_DOMAIN || 'localhost',
    BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET || '',
    BETTER_AUTH_URL: process.env.BETTER_AUTH_URL || 'http://localhost:10000',
    TRUSTED_ORIGINS: process.env.TRUSTED_ORIGINS?.split(',') || ['http://localhost:3000'],
    DATABASE_STRING: process.env.DATABASE_STRING || '',
    GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID || '',
    GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET || '',
    GITHUB_CLIENT_ID: process.env.GITHUB_CLIENT_ID || '',
    GITHUB_CLIENT_SECRET: process.env.GITHUB_CLIENT_SECRET || '',
    MICROSOFT_CLIENT_ID: process.env.MICROSOFT_CLIENT_ID || '',
    MICROSOFT_CLIENT_SECRET: process.env.MICROSOFT_CLIENT_SECRET || '',
    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID || '',
    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY || '',
    AWS_REGION: process.env.AWS_REGION || '',
    AWS_S3_BUCKET: process.env.AWS_S3_BUCKET || '',
    AWS_SENDER_EMAIL: process.env.AWS_SENDER_EMAIL || '',
    WEBHOOK_SECRET: process.env.WEBHOOK_SECRET || '',
    WEBHOOK_EP: process.env.WEBHOOK_EP || '',
  };
};

import dotenv from 'dotenv';

dotenv.config();
const config = getConfig();

export default config;