// import { NextResponse } from 'next/server';

// export async function POST(request: Request) {
//   try {
//     const body = await request.json();
    
//     // Pega a URL definida na Vercel ou usa localhost se não tiver
//     const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

//     console.log(`Encaminhando ${body.action} para: ${backendUrl}/api/trading/toggle`);

//     const response = await fetch(`${backendUrl}/api/trading/toggle`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(body),
//     });

//     if (!response.ok) {
//         return NextResponse.json({ error: 'Erro no Python' }, { status: response.status });
//     }

//     const data = await response.json();
//     return NextResponse.json(data);

//   } catch (error) {
//     return NextResponse.json({ error: 'Falha de conexão Next->Python' }, { status: 500 });
//   }
// }

import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:5000';

    const response = await fetch(`${backendUrl}/api/trading/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });

  } catch (error) {
    return NextResponse.json({ error: 'Erro ao comunicar com o robô' }, { status: 500 });
  }
}