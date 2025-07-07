export const createFullS3URL = (url: string) => {
  if (url.includes('s3.ap-south-1.amazonaws.com')) return url
  const config = useRuntimeConfig()

  return `${config.public.s3Url}${url}`;
};

export const getSubdomain = (): string | null => {
  try {
    const hostname = window.location.hostname
    const parsedUrl = new URL(hostname.includes('://') ? hostname : `https://${hostname}`);
    const hostParts = parsedUrl.hostname.split('.');

    if (hostParts.length >= 2) {
      return hostParts[0]; // Returns "abcd"
    }
    return null; // No subdomain found
  } catch (e) {
    console.error("Invalid URL:", e);
    return null;
  }
}