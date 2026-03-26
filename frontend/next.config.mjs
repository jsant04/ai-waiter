/** @type {import('next').NextConfig} */
const nextConfig = {
  // Expose env vars to the client bundle
  env: {
    NEXT_PUBLIC_API_URL:
      process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
    NEXT_PUBLIC_RESTAURANT_ID:
      process.env.NEXT_PUBLIC_RESTAURANT_ID ?? "default",
  },
  // Allow images from external domains if needed in the future
  images: {
    remotePatterns: [],
  },
};

export default nextConfig;
