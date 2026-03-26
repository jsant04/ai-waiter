/** @type {import('next').NextConfig} */
const nextConfig = {
  // NEXT_PUBLIC_* vars are automatically exposed to the browser by Next.js.
  // Set them in Vercel → Project → Environment Variables, or in .env.local locally.
  //
  // Vercel monorepo (vercel.json routes /api/* → Python backend):
  //   NEXT_PUBLIC_API_URL  → leave unset (relative URLs, same domain)
  //
  // Separate backend deployment (Railway / Render / etc.):
  //   NEXT_PUBLIC_API_URL  → https://your-backend.up.railway.app
  //   NEXT_PUBLIC_RESTAURANT_ID → default

  // Standalone output keeps the Lambda bundle small on Vercel
  output: "standalone",

  images: {
    remotePatterns: [],
  },
};

export default nextConfig;
