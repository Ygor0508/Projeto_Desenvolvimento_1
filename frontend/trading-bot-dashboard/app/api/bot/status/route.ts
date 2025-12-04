// import { NextResponse } from 'next/server';

// export async function GET() {
//   try {
//     const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';
    
//     const response = await fetch(`${backendUrl}/api/bot/status`, {
//         method: 'GET',
//         headers: { 'Content-Type': 'application/json' },
//         cache: 'no-store' // Importante para não cachear status antigo
//     });

//     const data = await response.json();
//     return NextResponse.json(data);
//   } catch (error) {
//     return NextResponse.json({ running: false }, { status: 200 });
//   }
// }




import { NextResponse } from 'next/server';

// Evita que a Vercel cacheie a resposta (o status muda em tempo real)
export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    // Usa a variável correta BACKEND_URL
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

    const response = await fetch(`${backendUrl}/api/bot/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store' // Garante que sempre busque o dado real
    });

    if (!response.ok) {
      console.error("Erro ao buscar status:", response.status);
      // Se der erro, assume que está parado para não quebrar a tela
      return NextResponse.json({ running: false, positions: {} });
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("Falha na rota de status:", error);
    return NextResponse.json({ running: false, error: 'Erro de conexão' }, { status: 500 });
  }
}