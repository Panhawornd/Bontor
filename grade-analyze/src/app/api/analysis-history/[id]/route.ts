import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'
import { revalidatePath } from 'next/cache'
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export async function DELETE(
  req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const rawCookie = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    const token = rawCookie?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const payload = verifyToken(token)
    if (!payload || typeof payload.userId !== 'number') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id: idStr } = await params
    const id = parseInt(idStr)
    
    console.log(`[DELETE History] Attempting to delete id: ${id} for user: ${payload.userId}`);

    if (isNaN(id)) {
        return NextResponse.json({ error: 'Invalid ID' }, { status: 400 })
    }

    // Verify ownership before deleting
    const recommendation = await prisma.recommendation.findUnique({
      where: { id },
      select: { userId: true },
    })

    if (!recommendation) {
      console.log(`[DELETE History] Recommendation ${id} not found`);
      return NextResponse.json({ error: 'Not found' }, { status: 404 })
    }

    if (recommendation.userId !== payload.userId) {
      console.log(`[DELETE History] Ownership mismatch: owner=${recommendation.userId}, requester=${payload.userId}`);
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Delete the recommendation
    // Database cascading (ON DELETE CASCADE) will automatically handle Grades and Inputs
    const deleted = await prisma.recommendation.delete({
      where: { id },
    })

    console.log(`[DELETE History] Successfully deleted recommendation ${deleted.id} and all cascaded data`);

    // Revalidate the history path
    revalidatePath('/history')
    revalidatePath('/dashboard')

    return NextResponse.json({ success: true, deletedId: id })
  } catch (error) {
    console.error('[DELETE History] Error:', error)
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })
  }
}
