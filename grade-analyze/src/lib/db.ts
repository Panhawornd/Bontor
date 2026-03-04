import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

function createPrismaClient() {
  const url = process.env.DATABASE_URL
  const connectionUrl = url
    ? url.includes('?')
      ? `${url}&connection_limit=5&pool_timeout=20`
      : `${url}?connection_limit=5&pool_timeout=20`
    : undefined

  return new PrismaClient({
    datasources: connectionUrl ? { db: { url: connectionUrl } } : undefined,
  })
}

export const prisma = globalForPrisma.prisma ?? createPrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
