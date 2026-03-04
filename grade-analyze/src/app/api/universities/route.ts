import { NextResponse } from "next/server";
import { prisma } from '@/lib/db';

export async function GET() {
  try {
    const universities = await prisma.university.findMany({
      orderBy: {
        id: 'asc'
      }
    });

    return NextResponse.json({ universities });
  } catch (error) {
    console.error("Error fetching universities:", error);
    return NextResponse.json(
      { error: "Failed to fetch universities" },
      { status: 500 }
    );
  }
}
