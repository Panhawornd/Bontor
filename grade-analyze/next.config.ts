import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    FASTAPI_URL: 'http://localhost:8000',
    DATABASE_URL: 'postgresql://postgres:baboo123@localhost:5433/grade_analyzer',
    REDIS_URL: 'redis://localhost:6379',
  },
  images: {
    domains: [
      "source.unsplash.com",
      "images.unsplash.com",
      "cdn.pixabay.com",
      "www.cadt.edu.kh",
      "cadt.edu.kh",
      "khmyreaderfriends.blogspot.com",
      "www.rupp.edu.kh",
      "www.researchgate.net",
      "academics-bucket-sj19asxm-prod.s3.ap-southeast-1.amazonaws.com", 
      "camtesol.org",
      "i.ytimg.com",
      "westernuniversity.edu.kh",
      "elbbl.rule.edu.kh",
      "bbu-webiste-space.sgp1.cdn.digitaloceanspaces.com",
      "uni24k.com",
      "www.aupp.edu.kh",
      "numer.digital",
      "uhs.edu.kh",
      "www.puc.edu.kh",
      "encrypted-tbn0.gstatic.com",
      "cdn.norton-u.com",
      "i.pinimg.com",
    ],
  },

  // ============================================
  // Security Headers
  // Protects against clickjacking, MIME sniffing,
  // XSS, and enforces HTTPS in production.
  // ============================================
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
            // Prevents your site from being embedded in an iframe
            // (blocks clickjacking attacks)
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
            // Prevents browsers from guessing the file type
            // (blocks MIME-type sniffing attacks)
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
            // Controls how much URL info is sent when navigating
            // to external sites (protects user privacy)
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
            // Tells older browsers to block detected XSS attacks
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
            // Disables access to camera, mic, and GPS
            // (your app doesn't need them)
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
            // Forces HTTPS for 1 year after first visit
            // (only effective in production with HTTPS)
          },
        ],
      },
    ]
  },
};


export default nextConfig;

