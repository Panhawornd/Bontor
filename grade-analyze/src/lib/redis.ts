import { createClient, RedisClientType } from 'redis';

/**
 * Redis client singleton for Next.js
 * Prevents multiple connections during hot-reloading in development
 */

const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';

const globalForRedis = global as unknown as {
  redis: RedisClientType | undefined;
};

export const redis =
  globalForRedis.redis ??
  createClient({
    url: redisUrl,
  });

if (process.env.NODE_ENV !== 'production') globalForRedis.redis = redis;

// Automatically connect if not already connected
if (!redis.isOpen) {
  redis.connect().catch((err) => {
    console.error('Redis connection error:', err);
  });
}

redis.on('error', (err) => {
  console.error('Redis client error:', err);
});

export default redis;
