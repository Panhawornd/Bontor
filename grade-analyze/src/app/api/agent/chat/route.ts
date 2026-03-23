import { NextResponse } from 'next/server'
import { prisma } from '@/lib/db'
import { verifyToken } from '@/lib/auth'
import { GoogleGenerativeAI } from '@google/generative-ai'

// Initialize Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '')

// System instruction for the agent
const SYSTEM_INSTRUCTION = `You are Bontor AI, a highly direct educational counselor.

RULES FOR RESPONSE STRUCTURE:
1. NO MARKDOWN: Never use bold (**) or headers (#). Use plain text only.
2. NO EXTRA CONTEXT: Only answer the EXACT question asked. If the user asks about a major, only provide info about that major. Do not add career paths or university recommendations unless they were part of the question.
3. CLEAR SEPARATION: Use simple new lines for structure instead of symbols.

UNIVERSITY KNOWLEDGE:
- Tech (SE/Data Science): CADT, ITC, RUPP.
- Law: RULE.
- Medicine: UHS, UP.
- Business: NUM, PUC, AUPP.

Guidelines:
1. ONLY answer questions about university majors, universities, and career paths in Cambodia.
2. If the user asks about anything out of scope, politely decline.
3. Be professional and concise.`

export async function POST(req: Request) {
  try {
    // JWT Authentication check
    const rawCookie = req.headers.get('cookie')
      ?.split(';')
      .find(c => c.trim().startsWith('auth-token='))
    const token = rawCookie?.split('=').slice(1).join('=')

    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const payload = verifyToken(token)
    if (!payload || typeof payload !== 'object' || !('userId' in payload)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const userId = payload.userId as number

    // Validate API key
    if (!process.env.GEMINI_API_KEY) {
      console.error('GEMINI_API_KEY is not configured')
      return NextResponse.json(
        { error: 'AI service is not configured. Please set GEMINI_API_KEY in .env' },
        { status: 503 }
      )
    }

    // Validate request body
    const body = await req.json()
    const { messages, sessionId } = body as {
      messages: { role: 'user' | 'assistant'; content: string }[]
      sessionId?: number
    }

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json({ error: 'Messages are required' }, { status: 400 })
    }

    // Security Check: If sessionId is provided, verify it belongs to this user
    if (sessionId) {
      const existingSession = await prisma.chatSession.findFirst({
        where: { id: sessionId, userId },
      })
      if (!existingSession) {
        return NextResponse.json({ error: 'Session not found or unauthorized' }, { status: 404 })
      }
    }

    // The last message is the current user input
    const lastMessage = messages[messages.length - 1]
    if (lastMessage.role !== 'user') {
      return NextResponse.json({ error: 'Last message must be from user' }, { status: 400 })
    }

    // Initialize the Gemini model
    const model = genAI.getGenerativeModel({
      model: 'gemini-2.5-flash',
      systemInstruction: SYSTEM_INSTRUCTION,
    })

    // Convert message history to Gemini format
    const geminiHistory = messages.slice(0, -1).map(msg => ({
      role: msg.role === 'user' ? 'user' as const : 'model' as const,
      parts: [{ text: msg.content }],
    }))

    // Start chat with history
    const chat = model.startChat({
      history: geminiHistory,
    })

    // Send the latest message
    const result = await chat.sendMessage(lastMessage.content)
    const response = result.response.text()

    // Save messages to the database
    let activeSessionId = sessionId

    if (!activeSessionId) {
      // Create a new session with the first message as the title
      const title = lastMessage.content.slice(0, 50) + (lastMessage.content.length > 50 ? '...' : '')
      const session = await prisma.chatSession.create({
        data: {
          userId,
          title,
        },
      })
      activeSessionId = session.id
    }

    // Save user message and assistant response
    await prisma.chatMessage.createMany({
      data: [
        { sessionId: activeSessionId, role: 'user', content: lastMessage.content },
        { sessionId: activeSessionId, role: 'assistant', content: response },
      ],
    })

    // Update session timestamp
    await prisma.chatSession.update({
      where: { id: activeSessionId },
      data: { updatedAt: new Date() },
    })

    return NextResponse.json({ message: response, sessionId: activeSessionId })
  } catch (error: unknown) {
    console.error('Agent chat error:', error)

    // Handle specific Gemini/Google AI errors
    const errorMessage = error instanceof Error ? error.message : String(error)
    const statusCode = (error as { status?: number })?.status || 500

    if (statusCode === 429 || errorMessage.includes('429') || errorMessage.includes('quota')) {
      return NextResponse.json(
        { 
          error: 'Rate limit exceeded or Quota reached. Please wait a few seconds or check your Gemini API quota at https://aistudio.google.com/' 
        },
        { status: 429 }
      )
    }

    if (errorMessage.includes('API_KEY')) {
      return NextResponse.json(
        { error: 'Invalid API key. Please check your GEMINI_API_KEY configuration.' },
        { status: 503 }
      )
    }

    if (errorMessage.includes('SAFETY')) {
      return NextResponse.json(
        { error: 'The response was blocked due to safety filters. Please rephrase your question.' },
        { status: 422 }
      )
    }

    return NextResponse.json(
      { error: 'Failed to get AI response: ' + (error instanceof Error ? error.message : 'Unknown error') },
      { status: 500 }
    )
  }
}
