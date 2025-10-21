import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    FASTAPI_URL: 'http://localhost:8000',
    DATABASE_URL: 'postgresql://postgres:baboo123@localhost:5433/grade_analyzer',
    REDIS_URL: 'redis://localhost:6379',
  },
};

export default nextConfig;
