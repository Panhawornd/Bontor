
import jwt from 'jsonwebtoken'

import bcrypt from 'bcryptjs'

const JWT_SECRET = process.env.JWT_SECRET

if (!JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required')
}

export interface User {
  id: number
  name: string
  email: string
}

export interface JWTPayload {
  userId: number
  email: string
  name: string
}

export function generateToken(user: User): string {
  const payload: JWTPayload = {
    userId: user.id,
    email: user.email,
    name: user.name
  }
  return jwt.sign(payload, JWT_SECRET!, { expiresIn: '24h' })
}

export function verifyToken(token: string): JWTPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET!, { algorithms: ['HS256'] }) as JWTPayload
  } catch {
    return null
  }
}

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 12)
}

export async function comparePassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash)
}
