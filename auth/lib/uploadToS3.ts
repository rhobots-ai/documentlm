import pkg from '@aws-sdk/client-s3';
import axios from 'axios';
import config from '../config.ts';

const {S3Client, PutObjectCommand, PutObjectCommandInput} = pkg;

// AWS S3 Configuration (TypeScript interface for config)
interface S3Config {
  region: string;
  credentials: {
    accessKeyId: string;
    secretAccessKey: string;
  }
}

// Function to upload image to S3
export const uploadImageToS3 = async (
  imageUrl: string,
  bucketName: string,
  s3Key: string
): Promise<string> => {
  const s3Config: S3Config = {
    region: 'ap-south-1',
    credentials: {
      accessKeyId: config.AWS_ACCESS_KEY_ID,
      secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
    }
  };

  const s3Client = new S3Client(s3Config);

  try {
    // 1. Fetch the image
    const response = await axios.get(imageUrl, {
      responseType: 'arraybuffer',
    });

    const imageBuffer = Buffer.from(response.data, 'binary');

    // 2. Prepare S3 upload parameters
    const uploadParams: PutObjectCommandInput = {
      Bucket: bucketName,
      Key: s3Key,
      Body: imageBuffer,
      ContentType: response.headers['content-type'],
      ACL: 'public-read'
    };

    // 3. Upload to S3
    await s3Client.send(new PutObjectCommand(uploadParams));

    // 4. Return the public S3 URL
    return `https://${bucketName}.s3.${s3Config.region}.amazonaws.com/${s3Key}`;
  } catch (error) {
    console.error('Error uploading image to S3:', error);
    throw error;
  }
}