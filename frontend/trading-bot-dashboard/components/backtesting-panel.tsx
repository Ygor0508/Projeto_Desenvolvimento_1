// "use client"

// import { useState } from "react"
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// import { Button } from "@/components/ui/button"
// import { Input } from "@/components/ui/input"
// import { Label } from "@/components/ui/label"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import { Progress } from "@/components/ui/progress"
// import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
// import { Play, BarChart3, TrendingUp, TrendingDown, DollarSign } from "lucide-react"

// interface BacktestResult {
//   totalReturn: number
//   totalTrades: number
//   winRate: number
//   maxDrawdown: number
//   sharpeRatio: number
//   profitFactor: number
//   chartData: Array<{
//     date: string
//     portfolio: number
//     benchmark: number
//   }>
// }

// export function BacktestingPanel() {
//   const [isRunning, setIsRunning] = useState(false)
//   const [progress, setProgress] = useState(0)
//   const [results, setResults] = useState<BacktestResult | null>(null)
//   const [startDate, setStartDate] = useState("2024-01-01")
//   const [endDate, setEndDate] = useState("2024-01-31")
//   const [initialCapital, setInitialCapital] = useState(10000)
//   const [selectedSymbol, setSelectedSymbol] = useState("BTCUSDT")

//   const runBacktest = async () => {
//     setIsRunning(true)
//     setProgress(0)
//     setResults(null)

//     // Simular progresso do backtest
//     const progressInterval = setInterval(() => {
//       setProgress((prev) => {
//         if (prev >= 100) {
//           clearInterval(progressInterval)
//           return 100
//         }
//         return prev + 10
//       })
//     }, 200)

//     // Simular resultado após 2 segundos
//     setTimeout(() => {
//       const mockResults: BacktestResult = {
//         totalReturn: 15.7,
//         totalTrades: 45,
//         winRate: 67.8,
//         maxDrawdown: -8.2,
//         sharpeRatio: 1.34,
//         profitFactor: 1.89,
//         chartData: Array.from({ length: 30 }, (_, i) => ({
//           date: `2024-01-${String(i + 1).padStart(2, "0")}`,
//           portfolio: initialCapital + (Math.random() * 2000 - 500) + i * 50,
//           benchmark: initialCapital + i * 30 + (Math.random() * 1000 - 500),
//         })),
//       }

//       setResults(mockResults)
//       setIsRunning(false)
//       clearInterval(progressInterval)
//     }, 2000)
//   }

//   return (
//     <div className="space-y-6">
//       {/* Configurações do Backtest */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader>
//           <CardTitle className="flex items-center gap-2 text-white">
//             <BarChart3 className="w-5 h-5" />
//             Configurações do Backtest
//           </CardTitle>
//           <CardDescription className="text-slate-400">
//             Configure os parâmetros para testar sua estratégia
//           </CardDescription>
//         </CardHeader>
//         <CardContent className="space-y-4">
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
//             <div className="space-y-2">
//               <Label htmlFor="symbol" className="text-slate-200">
//                 Símbolo
//               </Label>
//               <Select value={selectedSymbol} onValueChange={setSelectedSymbol}>
//                 <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
//                   <SelectValue />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="BTCUSDT">BTCUSDT</SelectItem>
//                   <SelectItem value="ETHUSDT">ETHUSDT</SelectItem>
//                   <SelectItem value="BNBUSDT">BNBUSDT</SelectItem>
//                   <SelectItem value="ALL">Todos os Símbolos</SelectItem>
//                 </SelectContent>
//               </Select>
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="startDate" className="text-slate-200">
//                 Data Inicial
//               </Label>
//               <Input
//                 id="startDate"
//                 type="date"
//                 value={startDate}
//                 onChange={(e) => setStartDate(e.target.value)}
//                 className="bg-slate-700 border-slate-600 text-white"
//               />
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="endDate" className="text-slate-200">
//                 Data Final
//               </Label>
//               <Input
//                 id="endDate"
//                 type="date"
//                 value={endDate}
//                 onChange={(e) => setEndDate(e.target.value)}
//                 className="bg-slate-700 border-slate-600 text-white"
//               />
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="capital" className="text-slate-200">
//                 Capital Inicial
//               </Label>
//               <Input
//                 id="capital"
//                 type="number"
//                 value={initialCapital}
//                 onChange={(e) => setInitialCapital(Number(e.target.value))}
//                 className="bg-slate-700 border-slate-600 text-white"
//                 min={1000}
//               />
//             </div>
//           </div>

//           <div className="flex gap-4">
//             <Button onClick={runBacktest} disabled={isRunning} className="flex items-center gap-2">
//               <Play className="w-4 h-4" />
//               {isRunning ? "Executando..." : "Executar Backtest"}
//             </Button>
//           </div>

//           {isRunning && (
//             <div className="space-y-2">
//               <div className="flex justify-between text-sm text-slate-400">
//                 <span>Progresso do Backtest</span>
//                 <span>{progress}%</span>
//               </div>
//               <Progress value={progress} className="w-full" />
//             </div>
//           )}
//         </CardContent>
//       </Card>

//       {/* Resultados */}
//       {results && (
//         <>
//           {/* Métricas de Performance */}
//           <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Retorno Total</CardTitle>
//                 <TrendingUp className="h-4 w-4 text-green-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-green-500">
//                   {results.totalReturn > 0 ? "+" : ""}
//                   {results.totalReturn.toFixed(1)}%
//                 </div>
//               </CardContent>
//             </Card>

//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Total de Trades</CardTitle>
//                 <BarChart3 className="h-4 w-4 text-blue-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-white">{results.totalTrades}</div>
//               </CardContent>
//             </Card>

//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Taxa de Acerto</CardTitle>
//                 <TrendingUp className="h-4 w-4 text-green-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-white">{results.winRate.toFixed(1)}%</div>
//               </CardContent>
//             </Card>

//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Max Drawdown</CardTitle>
//                 <TrendingDown className="h-4 w-4 text-red-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-red-500">{results.maxDrawdown.toFixed(1)}%</div>
//               </CardContent>
//             </Card>

//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Sharpe Ratio</CardTitle>
//                 <BarChart3 className="h-4 w-4 text-blue-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-white">{results.sharpeRatio.toFixed(2)}</div>
//               </CardContent>
//             </Card>

//             <Card className="bg-slate-800 border-slate-700">
//               <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//                 <CardTitle className="text-sm font-medium text-slate-200">Profit Factor</CardTitle>
//                 <DollarSign className="h-4 w-4 text-green-500" />
//               </CardHeader>
//               <CardContent>
//                 <div className="text-2xl font-bold text-white">{results.profitFactor.toFixed(2)}</div>
//               </CardContent>
//             </Card>
//           </div>

//           {/* Gráfico de Performance */}
//           <Card className="bg-slate-800 border-slate-700">
//             <CardHeader>
//               <CardTitle className="text-white">Performance vs Benchmark</CardTitle>
//               <CardDescription className="text-slate-400">Comparação da estratégia com buy & hold</CardDescription>
//             </CardHeader>
//             <CardContent>
//               <ResponsiveContainer width="100%" height={400}>
//                 <LineChart data={results.chartData}>
//                   <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
//                   <XAxis dataKey="date" stroke="#9CA3AF" />
//                   <YAxis stroke="#9CA3AF" />
//                   <Tooltip
//                     contentStyle={{
//                       backgroundColor: "#1F2937",
//                       border: "1px solid #374151",
//                       borderRadius: "8px",
//                     }}
//                   />
//                   <Line
//                     type="monotone"
//                     dataKey="portfolio"
//                     stroke="#10B981"
//                     strokeWidth={2}
//                     name="Estratégia"
//                     dot={false}
//                   />
//                   <Line
//                     type="monotone"
//                     dataKey="benchmark"
//                     stroke="#6B7280"
//                     strokeWidth={2}
//                     strokeDasharray="5 5"
//                     name="Buy & Hold"
//                     dot={false}
//                   />
//                 </LineChart>
//               </ResponsiveContainer>
//             </CardContent>
//           </Card>
//         </>
//       )}
//     </div>
//   )
// }









"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Loader2, PlayCircle, TrendingUp, TrendingDown, Activity } from "lucide-react"
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { useToast } from "@/components/ui/use-toast"

export function BacktestingPanel() {
  const [symbol, setSymbol] = useState("BTCUSDT")
  // Estado para armazenar a lista que vem do robô
  const [availableSymbols, setAvailableSymbols] = useState<string[]>([])
  const [isLoadingSymbols, setIsLoadingSymbols] = useState(false)
  const [testPeriod, setTestPeriod] = useState("60") // Padrão 60 dias para não travar
  
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const { toast } = useToast()

  // 1. Busca os símbolos que o robô identificou ao carregar a página
  useEffect(() => {
    const fetchSymbols = async () => {
      setIsLoadingSymbols(true)
      try {
        const response = await fetch('/api/symbols')
        if (response.ok) {
          const data = await response.json()
          
          // 2. Adiciona a opção "TODOS" manualmente no início da lista
          // Se o backend retornar lista vazia (fallback), garantimos pelo menos o BTC
          const listaFinal = data.length > 0 ? ["TODOS", ...data] : ["TODOS", "BTCUSDT", "ETHUSDT"]
          
          setAvailableSymbols(listaFinal)
          // Seleciona o primeiro ativo real por padrão (pula o TODOS se quiser) ou mantém BTC
          if (data.includes("BTCUSDT")) setSymbol("BTCUSDT")
          else if (data.length > 0) setSymbol(data[0])
          
        } else {
            // Fallback visual caso a API falhe mas não quebre a tela
            setAvailableSymbols(["TODOS", "BTCUSDT", "ETHUSDT"])
        }
      } catch (error) {
        console.error("Erro ao buscar símbolos", error)
        toast({ title: "Aviso", description: "Usando lista padrão de ativos." })
        setAvailableSymbols(["TODOS", "BTCUSDT", "ETHUSDT"])
      } finally {
        setIsLoadingSymbols(false)
      }
    }
    fetchSymbols()
  }, [])

  const runBacktest = async () => {
    setIsRunning(true)
    setResults(null)

    // Lógica para lidar com "TODOS" ou ativo único
    let symbolToRun = symbol;
    if (symbol === "TODOS") {
        toast({ title: "Info", description: "Rodando backtest no ativo principal (BTCUSDT) para demonstração." })
        symbolToRun = "BTCUSDT"; 
    }

    try {
      const response = await fetch('/api/backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Reduzimos para 60 dias ou o valor selecionado para evitar timeout
        body: JSON.stringify({ symbol: symbolToRun, period: parseInt(testPeriod) })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Erro no backtest")
      }

      const data = await response.json()
      setResults(data)
      toast({ title: "Sucesso", description: `Backtest de ${symbolToRun} concluído.` })
      
    } catch (error) {
      console.error(error)
      toast({ 
        title: "Erro", 
        description: "Falha ao rodar backtest. Tente um período menor de dias.", 
        variant: "destructive" 
      })
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <Card className="col-span-4 bg-slate-800 border-slate-700">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-white">
          <Activity className="h-5 w-5" /> Backtest & Simulação
        </CardTitle>
        <CardDescription className="text-slate-400">
          Teste a estratégia em dados históricos com os ativos identificados pelo Robô
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4">
          <div className="flex flex-wrap items-center gap-4">
            
            {/* Seletor de Moeda */}
            <div className="w-[200px]">
                <Select value={symbol} onValueChange={setSymbol} disabled={isLoadingSymbols}>
                <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder={isLoadingSymbols ? "Carregando..." : "Selecione o Ativo"} />
                </SelectTrigger>
                <SelectContent className="bg-slate-700 border-slate-600 text-white">
                    {availableSymbols.map((s) => (
                        <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                </SelectContent>
                </Select>
            </div>

            {/* Seletor de Dias */}
            <div className="w-[150px]">
                <Select value={testPeriod} onValueChange={setTestPeriod}>
                <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Dias" />
                </SelectTrigger>
                <SelectContent className="bg-slate-700 border-slate-600 text-white">
                    <SelectItem value="30">30 Dias (Rápido)</SelectItem>
                    <SelectItem value="60">60 Dias (Padrão)</SelectItem>
                    <SelectItem value="90">90 Dias</SelectItem>
                    <SelectItem value="180">180 Dias (Lento)</SelectItem>
                </SelectContent>
                </Select>
            </div>

            <Button onClick={runBacktest} disabled={isRunning} className="bg-blue-600 hover:bg-blue-700 text-white">
              {isRunning ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <PlayCircle className="mr-2 h-4 w-4" />}
              Rodar Backtest
            </Button>
          </div>

          {results && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {/* Card Lucro */}
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Lucro Total</div>
                  <div className={`text-2xl font-bold ${results.total_pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    ${results.total_pnl}
                  </div>
                </div>
                {/* Card Win Rate */}
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Win Rate</div>
                  <div className="text-2xl font-bold text-white">{results.win_rate}%</div>
                </div>
                {/* Card Trades */}
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Trades</div>
                  <div className="text-2xl font-bold text-white">{results.total_trades}</div>
                </div>
                {/* Card Regime */}
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Regime Macro</div>
                  <div className="flex items-center gap-2 text-2xl font-bold">
                    {results.regime === "BULLISH" ? 
                      <><TrendingUp className="text-green-500 h-6 w-6" /> <span className="text-green-500">Alta</span></> : 
                      <><TrendingDown className="text-red-500 h-6 w-6" /> <span className="text-red-500">Baixa</span></>
                    }
                  </div>
                </div>
              </div>

              <div className="h-[300px] w-full border border-slate-700 rounded-lg p-4 bg-slate-900/50">
                <h4 className="mb-4 text-sm font-medium text-slate-200">Curva de Patrimônio</h4>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={results.equity_curve}>
                    <defs>
                      <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.5} />
                    <XAxis dataKey="time" hide />
                    <YAxis domain={['auto', 'auto']} stroke="#9CA3AF" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', color: '#fff' }}
                      labelStyle={{ color: '#9ca3af' }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="value" 
                      stroke="#10b981" 
                      fillOpacity={1} 
                      fill="url(#colorValue)" 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}