import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // AQUI ESTÁ A CORREÇÃO: Usando BACKEND_URL conforme sua configuração no Vercel
    const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:5000';

    const response = await fetch(`${backendUrl}/api/config/api-keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });

  } catch (error) {
    return NextResponse.json({ error: 'Falha ao conectar com o servidor Python' }, { status: 500 });
  }
}