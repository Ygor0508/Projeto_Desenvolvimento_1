import { NextResponse } from 'next/server';

// Evita cache para garantir dados frescos
export const dynamic = 'force-dynamic';

export async function POST(request: Request) {
  try {
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';
    const body = await request.json();

    const response = await fetch(`${backendUrl}/api/backtest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });

  } catch (error) {
    console.error("Erro no proxy de backtest:", error);
    return NextResponse.json({ error: 'Falha ao conectar com o servidor Python' }, { status: 500 });
  }
}