// "use client"

// import { useState, useEffect } from "react"
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// import { Badge } from "@/components/ui/badge"
// import { Progress } from "@/components/ui/progress"
// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

// interface Position {
//   symbol: string
//   quantity: number
//   entryPrice: number
//   currentPrice: number
//   pnl: number
//   pnlPercent: number
// }

// interface MarketData {
//   symbol: string
//   price: number
//   change24h: number
//   volume: number
//   signal: "BUY" | "SELL" | "HOLD"
//   rsi: number
//   confidence: number
// }

// export function RealTradingDashboard() {
//   const [positions, setPositions] = useState<Position[]>([])
//   const [marketData, setMarketData] = useState<MarketData[]>([])
//   const [priceHistory, setPriceHistory] = useState<any[]>([])
//   const [isLoading, setIsLoading] = useState(true)
//   const [accountInfo, setAccountInfo] = useState<any>(null)

//   useEffect(() => {
//     const fetchRealData = async () => {
//       try {
//         setIsLoading(true)

//         // Buscar informações da conta real
//         const accountResponse = await fetch("/api/binance/account")
//         const accountData = await accountResponse.json()
//         setAccountInfo(accountData)

//         // Buscar posições reais
//         const positionsResponse = await fetch("/api/binance/positions")
//         const positionsData = await positionsResponse.json()
//         setPositions(positionsData.positions || [])

//         // Buscar dados de mercado reais
//         const marketResponse = await fetch("/api/binance/market-data")
//         const marketDataReal = await marketResponse.json()
//         setMarketData(marketDataReal.data || [])

//         // Buscar histórico de preços real
//         const historyResponse = await fetch("/api/binance/price-history")
//         const historyData = await historyResponse.json()
//         setPriceHistory(historyData.history || [])

//         setIsLoading(false)
//       } catch (error) {
//         console.error("Erro ao carregar dados reais:", error)
//         setIsLoading(false)
//       }
//     }

//     fetchRealData()
//     const interval = setInterval(fetchRealData, 30000) // Atualizar a cada 30 segundos

//     return () => clearInterval(interval)
//   }, [])

//   if (isLoading) {
//     return (
//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {[...Array(4)].map((_, i) => (
//           <Card key={i} className="bg-slate-800 border-slate-700">
//             <CardContent className="p-6">
//               <div className="animate-pulse space-y-4">
//                 <div className="h-4 bg-slate-700 rounded w-1/4"></div>
//                 <div className="h-8 bg-slate-700 rounded w-1/2"></div>
//                 <div className="h-32 bg-slate-700 rounded"></div>
//               </div>
//             </CardContent>
//           </Card>
//         ))}
//       </div>
//     )
//   }

//   return (
//     <div className="space-y-6">
//       {/* Informações da Conta Real */}
//       {accountInfo && (
//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader>
//             <CardTitle className="text-white">Informações da Conta Binance</CardTitle>
//             <CardDescription className="text-slate-400">Dados reais da sua conta</CardDescription>
//           </CardHeader>
//           <CardContent>
//             <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//               <div className="p-4 bg-slate-700 rounded-lg">
//                 <h4 className="font-semibold text-white">Saldo Total</h4>
//                 <p className="text-2xl font-bold text-green-500">
//                   ${Number.parseFloat(accountInfo.totalWalletBalance || 0).toFixed(2)}
//                 </p>
//               </div>
//               <div className="p-4 bg-slate-700 rounded-lg">
//                 <h4 className="font-semibold text-white">Saldo Disponível</h4>
//                 <p className="text-2xl font-bold text-blue-500">
//                   ${Number.parseFloat(accountInfo.availableBalance || 0).toFixed(2)}
//                 </p>
//               </div>
//               <div className="p-4 bg-slate-700 rounded-lg">
//                 <h4 className="font-semibold text-white">Pode Operar</h4>
//                 <p className="text-2xl font-bold text-white">{accountInfo.canTrade ? "✅ Sim" : "❌ Não"}</p>
//               </div>
//             </div>
//           </CardContent>
//         </Card>
//       )}

//       {/* Posições Reais */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader>
//           <CardTitle className="text-white">Posições Abertas (Reais)</CardTitle>
//           <CardDescription className="text-slate-400">Suas posições atuais na Binance</CardDescription>
//         </CardHeader>
//         <CardContent>
//           {positions.length > 0 ? (
//             <div className="space-y-4">
//               {positions.map((position) => (
//                 <div key={position.symbol} className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
//                   <div className="flex items-center gap-4">
//                     <div>
//                       <h4 className="font-semibold text-white">{position.symbol}</h4>
//                       <p className="text-sm text-slate-400">
//                         {position.quantity} @ ${position.entryPrice.toLocaleString()}
//                       </p>
//                     </div>
//                   </div>
//                   <div className="text-right">
//                     <div className={`font-semibold ${position.pnl >= 0 ? "text-green-500" : "text-red-500"}`}>
//                       ${Math.abs(position.pnl).toFixed(2)}
//                     </div>
//                     <div className={`text-sm ${position.pnl >= 0 ? "text-green-400" : "text-red-400"}`}>
//                       {position.pnlPercent >= 0 ? "+" : ""}
//                       {position.pnlPercent.toFixed(2)}%
//                     </div>
//                   </div>
//                 </div>
//               ))}
//             </div>
//           ) : (
//             <div className="text-center py-8 text-slate-400">Nenhuma posição aberta no momento</div>
//           )}
//         </CardContent>
//       </Card>

//       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//         {/* Gráfico de Performance Real */}
//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader>
//             <CardTitle className="text-white">Performance do Portfólio (Real)</CardTitle>
//             <CardDescription className="text-slate-400">Dados reais das últimas 24 horas</CardDescription>
//           </CardHeader>
//           <CardContent>
//             {priceHistory.length > 0 ? (
//               <ResponsiveContainer width="100%" height={300}>
//                 <LineChart data={priceHistory}>
//                   <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
//                   <XAxis dataKey="time" stroke="#9CA3AF" />
//                   <YAxis stroke="#9CA3AF" />
//                   <Tooltip
//                     contentStyle={{
//                       backgroundColor: "#1F2937",
//                       border: "1px solid #374151",
//                       borderRadius: "8px",
//                     }}
//                   />
//                   <Line type="monotone" dataKey="portfolio" stroke="#10B981" strokeWidth={2} dot={false} />
//                 </LineChart>
//               </ResponsiveContainer>
//             ) : (
//               <div className="h-[300px] flex items-center justify-center text-slate-400">
//                 Carregando dados de performance...
//               </div>
//             )}
//           </CardContent>
//         </Card>

//         {/* Sinais de Trading Reais */}
//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader>
//             <CardTitle className="text-white">Sinais de Trading (Reais)</CardTitle>
//             <CardDescription className="text-slate-400">Análise em tempo real dos mercados</CardDescription>
//           </CardHeader>
//           <CardContent>
//             {marketData.length > 0 ? (
//               <div className="space-y-4">
//                 {marketData.map((data) => (
//                   <div key={data.symbol} className="flex items-center justify-between p-3 bg-slate-700 rounded-lg">
//                     <div>
//                       <h4 className="font-semibold text-white">{data.symbol}</h4>
//                       <p className="text-sm text-slate-400">${data.price.toLocaleString()}</p>
//                     </div>
//                     <div className="flex items-center gap-3">
//                       <div className="text-right">
//                         <Badge
//                           variant={
//                             data.signal === "BUY" ? "default" : data.signal === "SELL" ? "destructive" : "secondary"
//                           }
//                           className="mb-1"
//                         >
//                           {data.signal}
//                         </Badge>
//                         <div className="text-xs text-slate-400">Confiança: {(data.confidence * 100).toFixed(0)}%</div>
//                       </div>
//                       <div className="w-16">
//                         <Progress value={data.rsi} className="h-2" />
//                         <div className="text-xs text-slate-400 mt-1">RSI: {data.rsi}</div>
//                       </div>
//                     </div>
//                   </div>
//                 ))}
//               </div>
//             ) : (
//               <div className="text-center py-8 text-slate-400">Carregando sinais de mercado...</div>
//             )}
//           </CardContent>
//         </Card>
//       </div>

//       {/* Análise de Volume Real */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader>
//           <CardTitle className="text-white">Análise de Volume (Real)</CardTitle>
//           <CardDescription className="text-slate-400">Volume de negociação real por ativo</CardDescription>
//         </CardHeader>
//         <CardContent>
//           {marketData.length > 0 ? (
//             <ResponsiveContainer width="100%" height={200}>
//               <BarChart data={marketData}>
//                 <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
//                 <XAxis dataKey="symbol" stroke="#9CA3AF" />
//                 <YAxis stroke="#9CA3AF" />
//                 <Tooltip
//                   contentStyle={{
//                     backgroundColor: "#1F2937",
//                     border: "1px solid #374151",
//                     borderRadius: "8px",
//                   }}
//                 />
//                 <Bar dataKey="volume" fill="#3B82F6" />
//               </BarChart>
//             </ResponsiveContainer>
//           ) : (
//             <div className="h-[200px] flex items-center justify-center text-slate-400">
//               Carregando dados de volume...
//             </div>
//           )}
//         </CardContent>
//       </Card>
//     </div>
//   )
// }



"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button" // Novo
import { PlayCircle, StopCircle, RefreshCw, Power } from "lucide-react" // Novos Ícones
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

interface Position {
  symbol: string
  quantity: number
  entryPrice: number
  currentPrice: number
  pnl: number
  pnlPercent: number
}

interface MarketData {
  symbol: string
  price: number
  change24h: number
  volume: number
  signal: "BUY" | "SELL" | "HOLD"
  rsi: number
  confidence: number
}

export function RealTradingDashboard() {
  // --- Estados de Dados (Originais) ---
  const [positions, setPositions] = useState<Position[]>([])
  const [marketData, setMarketData] = useState<MarketData[]>([])
  const [priceHistory, setPriceHistory] = useState<any[]>([])
  const [accountInfo, setAccountInfo] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  // --- Novos Estados de Controle (Para o Botão) ---
  const [isRunning, setIsRunning] = useState(false)
  const [isToggling, setIsToggling] = useState(false)

  // --- Função para Ligar/Desligar o Robô (Nova) ---
  const toggleBot = async () => {
    setIsToggling(true)
    const action = isRunning ? "stop" : "start"
    
    try {
      // Chama a rota Proxy que criamos
      const response = await fetch("/api/trading/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      })

      if (!response.ok) throw new Error("Falha na comunicação")

      const data = await response.json()
      
      // Atualiza o visual
      if (data.status === 'started') setIsRunning(true)
      if (data.status === 'stopped') setIsRunning(false)

    } catch (error) {
      console.error("Erro ao alterar status do robô:", error)
      alert("Erro ao conectar com o servidor. Verifique se o Python está rodando.")
    } finally {
      setIsToggling(false)
    }
  }

  // --- Função de Busca de Dados (Atualizada) ---
  const fetchRealData = async () => {
    try {
      // Não ativamos isLoading(true) aqui para não piscar a tela no refresh automático

      // 1. Checa status do robô
      try {
        const statusRes = await fetch("/api/bot/status")
        if (statusRes.ok) {
            const statusData = await statusRes.json()
            setIsRunning(statusData.running)
        }
      } catch (e) { console.log("Erro ao buscar status", e) }

      // 2. Busca dados da Binance (Seu código original)
      const accountResponse = await fetch("/api/binance/account")
      const accountData = await accountResponse.json()
      setAccountInfo(accountData)

      const positionsResponse = await fetch("/api/binance/positions")
      const positionsData = await positionsResponse.json()
      setPositions(positionsData.positions || [])

      const marketResponse = await fetch("/api/binance/market-data")
      const marketDataReal = await marketResponse.json()
      setMarketData(marketDataReal.data || [])

      const historyResponse = await fetch("/api/binance/price-history")
      const historyData = await historyResponse.json()
      setPriceHistory(historyData.history || [])

      setIsLoading(false)
    } catch (error) {
      console.error("Erro ao carregar dados reais:", error)
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchRealData()
    const interval = setInterval(fetchRealData, 10000) // 10 segundos
    return () => clearInterval(interval)
  }, [])

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="bg-slate-800 border-slate-700">
            <CardContent className="p-6">
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-slate-700 rounded w-1/4"></div>
                <div className="h-8 bg-slate-700 rounded w-1/2"></div>
                <div className="h-32 bg-slate-700 rounded"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      
      {/* --- NOVO: Painel de Controle (Botões) --- */}
      <div className="flex flex-col md:flex-row justify-between items-center bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
        <div className="flex items-center gap-4">
            <div className={`p-3 rounded-full ${isRunning ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
                <Power className="h-6 w-6" />
            </div>
            <div>
                <h2 className="text-2xl font-bold text-white">Status do Robô</h2>
                <div className="flex items-center gap-2">
                    <span className={`h-2.5 w-2.5 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
                    <span className="text-slate-400 font-medium">{isRunning ? "SISTEMA ONLINE" : "SISTEMA PARADO"}</span>
                </div>
            </div>
        </div>
        
        <div className="flex gap-3 mt-4 md:mt-0 w-full md:w-auto">
            <Button onClick={fetchRealData} variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800 flex-1 md:flex-none">
                <RefreshCw className="mr-2 h-4 w-4" /> Atualizar
            </Button>

            <Button 
                onClick={toggleBot} 
                disabled={isToggling}
                className={`flex-1 md:flex-none font-bold text-white transition-all ${
                    isRunning 
                    ? "bg-red-600 hover:bg-red-700 shadow-red-900/20" 
                    : "bg-green-600 hover:bg-green-700 shadow-green-900/20"
                }`}
            >
                {isToggling ? (
                    "Processando..."
                ) : isRunning ? (
                    <><StopCircle className="mr-2 h-5 w-5" /> PARAR ROBÔ</>
                ) : (
                    <><PlayCircle className="mr-2 h-5 w-5" /> INICIAR ROBÔ</>
                )}
            </Button>
        </div>
      </div>

      {/* Informações da Conta Real */}
      {accountInfo && (
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">Informações da Conta Binance</CardTitle>
            <CardDescription className="text-slate-400">Dados reais da sua conta</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-700 rounded-lg">
                <h4 className="font-semibold text-white">Saldo Total</h4>
                <p className="text-2xl font-bold text-green-500">
                  ${Number.parseFloat(accountInfo.totalWalletBalance || 0).toFixed(2)}
                </p>
              </div>
              <div className="p-4 bg-slate-700 rounded-lg">
                <h4 className="font-semibold text-white">Saldo Disponível</h4>
                <p className="text-2xl font-bold text-blue-500">
                  ${Number.parseFloat(accountInfo.availableBalance || 0).toFixed(2)}
                </p>
              </div>
              <div className="p-4 bg-slate-700 rounded-lg">
                <h4 className="font-semibold text-white">Pode Operar</h4>
                <p className="text-2xl font-bold text-white">{accountInfo.canTrade ? "✅ Sim" : "❌ Não"}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Posições Reais */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Posições Abertas (Reais)</CardTitle>
          <CardDescription className="text-slate-400">Suas posições atuais na Binance</CardDescription>
        </CardHeader>
        <CardContent>
          {positions.length > 0 ? (
            <div className="space-y-4">
              {positions.map((position) => (
                <div key={position.symbol} className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
                  <div className="flex items-center gap-4">
                    <div>
                      <h4 className="font-semibold text-white">{position.symbol}</h4>
                      <p className="text-sm text-slate-400">
                        {position.quantity} @ ${position.entryPrice.toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`font-semibold ${position.pnl >= 0 ? "text-green-500" : "text-red-500"}`}>
                      ${Math.abs(position.pnl).toFixed(2)}
                    </div>
                    <div className={`text-sm ${position.pnl >= 0 ? "text-green-400" : "text-red-400"}`}>
                      {position.pnlPercent >= 0 ? "+" : ""}
                      {position.pnlPercent.toFixed(2)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-400">Nenhuma posição aberta no momento</div>
          )}
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de Performance Real */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">Performance do Portfólio (Real)</CardTitle>
            <CardDescription className="text-slate-400">Dados reais das últimas 24 horas</CardDescription>
          </CardHeader>
          <CardContent>
            {priceHistory.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={priceHistory}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="time" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1F2937",
                      border: "1px solid #374151",
                      borderRadius: "8px",
                    }}
                  />
                  <Line type="monotone" dataKey="portfolio" stroke="#10B981" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-slate-400">
                Carregando dados de performance...
              </div>
            )}
          </CardContent>
        </Card>

        {/* Sinais de Trading Reais */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">Sinais de Trading (Reais)</CardTitle>
            <CardDescription className="text-slate-400">Análise em tempo real dos mercados</CardDescription>
          </CardHeader>
          <CardContent>
            {marketData.length > 0 ? (
              <div className="space-y-4">
                {marketData.map((data) => (
                  <div key={data.symbol} className="flex items-center justify-between p-3 bg-slate-700 rounded-lg">
                    <div>
                      <h4 className="font-semibold text-white">{data.symbol}</h4>
                      <p className="text-sm text-slate-400">${data.price.toLocaleString()}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <Badge
                          variant={
                            data.signal === "BUY" ? "default" : data.signal === "SELL" ? "destructive" : "secondary"
                          }
                          className="mb-1"
                        >
                          {data.signal}
                        </Badge>
                        <div className="text-xs text-slate-400">Confiança: {(data.confidence * 100).toFixed(0)}%</div>
                      </div>
                      <div className="w-16">
                        <Progress value={data.rsi} className="h-2" />
                        <div className="text-xs text-slate-400 mt-1">RSI: {data.rsi}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-400">Carregando sinais de mercado...</div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Análise de Volume Real (Recuperado) */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Análise de Volume (Real)</CardTitle>
          <CardDescription className="text-slate-400">Volume de negociação real por ativo</CardDescription>
        </CardHeader>
        <CardContent>
          {marketData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={marketData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="symbol" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1F2937",
                    border: "1px solid #374151",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="volume" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[200px] flex items-center justify-center text-slate-400">
              Carregando dados de volume...
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}