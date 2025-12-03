import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';
    
    const response = await fetch(`${backendUrl}/api/bot/status`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        cache: 'no-store' // Importante para não cachear status antigo
    });

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ running: false }, { status: 200 });
  }
}