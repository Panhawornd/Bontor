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

         // <-- Add this!
    ],
  },
};


export default nextConfig;
