// "use client"

// import { useState, useEffect } from "react"
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// import { Badge } from "@/components/ui/badge"
// import { Button } from "@/components/ui/button"
// import { Input } from "@/components/ui/input"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// import { Download, Filter, TrendingUp, TrendingDown, RefreshCw } from "lucide-react"

// interface RealTrade {
//   id: string
//   symbol: string
//   side: "BUY" | "SELL"
//   quantity: number
//   price: number
//   quoteQty: number
//   commission: number
//   commissionAsset: string
//   time: number
//   isBuyer: boolean
//   isMaker: boolean
//   isBestMatch: boolean
// }

// export function RealTradeHistory() {
//   const [trades, setTrades] = useState<RealTrade[]>([])
//   const [filteredTrades, setFilteredTrades] = useState<RealTrade[]>([])
//   const [filterSymbol, setFilterSymbol] = useState("all")
//   const [filterSide, setFilterSide] = useState("all")
//   const [searchTerm, setSearchTerm] = useState("")
//   const [isLoading, setIsLoading] = useState(true)
//   const [isRefreshing, setIsRefreshing] = useState(false)
//   const [stats, setStats] = useState({
//     totalPnL: 0,
//     totalTrades: 0,
//     winRate: 0,
//     totalCommission: 0,
//   })

//   const fetchRealTrades = async () => {
//     try {
//       setIsRefreshing(true)
//       const response = await fetch("/api/binance/trade-history")
//       const data = await response.json()

//       if (data.success) {
//         setTrades(data.trades)
//         setStats(data.stats)
//       } else {
//         console.error("Erro ao carregar trades:", data.error)
//       }
//     } catch (error) {
//       console.error("Erro ao buscar histórico de trades:", error)
//     } finally {
//       setIsLoading(false)
//       setIsRefreshing(false)
//     }
//   }

//   useEffect(() => {
//     fetchRealTrades()
//   }, [])

//   useEffect(() => {
//     let filtered = trades

//     if (filterSymbol !== "all") {
//       filtered = filtered.filter((trade) => trade.symbol === filterSymbol)
//     }

//     if (filterSide !== "all") {
//       filtered = filtered.filter((trade) => trade.side === filterSide)
//     }

//     if (searchTerm) {
//       filtered = filtered.filter(
//         (trade) => trade.symbol.toLowerCase().includes(searchTerm.toLowerCase()) || trade.id.includes(searchTerm),
//       )
//     }

//     setFilteredTrades(filtered)
//   }, [trades, filterSymbol, filterSide, searchTerm])

//   const exportTrades = () => {
//     const csvContent = [
//       ["ID", "Símbolo", "Lado", "Quantidade", "Preço", "Total", "Comissão", "Data"],
//       ...filteredTrades.map((trade) => [
//         trade.id,
//         trade.symbol,
//         trade.side,
//         trade.quantity.toString(),
//         trade.price.toString(),
//         trade.quoteQty.toString(),
//         `${trade.commission} ${trade.commissionAsset}`,
//         new Date(trade.time).toLocaleString(),
//       ]),
//     ]
//       .map((row) => row.join(","))
//       .join("\n")

//     const blob = new Blob([csvContent], { type: "text/csv" })
//     const url = window.URL.createObjectURL(blob)
//     const a = document.createElement("a")
//     a.href = url
//     a.download = `binance-trades-${new Date().toISOString().split("T")[0]}.csv`
//     a.click()
//     window.URL.revokeObjectURL(url)
//   }

//   const uniqueSymbols = [...new Set(trades.map((trade) => trade.symbol))]

//   if (isLoading) {
//     return (
//       <Card className="bg-slate-800 border-slate-700">
//         <CardContent className="p-6">
//           <div className="animate-pulse space-y-4">
//             <div className="h-4 bg-slate-700 rounded w-1/4"></div>
//             <div className="h-8 bg-slate-700 rounded w-1/2"></div>
//             <div className="space-y-2">
//               {[...Array(5)].map((_, i) => (
//                 <div key={i} className="h-12 bg-slate-700 rounded"></div>
//               ))}
//             </div>
//           </div>
//         </CardContent>
//       </Card>
//     )
//   }

//   return (
//     <div className="space-y-6">
//       {/* Estatísticas Reais */}
//       <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">P&L Total</CardTitle>
//             {stats.totalPnL >= 0 ? (
//               <TrendingUp className="h-4 w-4 text-green-500" />
//             ) : (
//               <TrendingDown className="h-4 w-4 text-red-500" />
//             )}
//           </CardHeader>
//           <CardContent>
//             <div className={`text-2xl font-bold ${stats.totalPnL >= 0 ? "text-green-500" : "text-red-500"}`}>
//               ${Math.abs(stats.totalPnL).toFixed(2)}
//             </div>
//             <p className="text-xs text-slate-400">{stats.totalPnL >= 0 ? "Lucro" : "Prejuízo"} acumulado</p>
//           </CardContent>
//         </Card>

//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Total de Trades</CardTitle>
//             <Filter className="h-4 w-4 text-blue-500" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-white">{stats.totalTrades}</div>
//             <p className="text-xs text-slate-400">Operações realizadas</p>
//           </CardContent>
//         </Card>

//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Taxa de Acerto</CardTitle>
//             <TrendingUp className="h-4 w-4 text-green-500" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-white">{stats.winRate.toFixed(1)}%</div>
//             <p className="text-xs text-slate-400">Trades vencedores</p>
//           </CardContent>
//         </Card>

//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Comissões Pagas</CardTitle>
//             <TrendingDown className="h-4 w-4 text-red-500" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-red-400">${stats.totalCommission.toFixed(2)}</div>
//             <p className="text-xs text-slate-400">Total em taxas</p>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Histórico Real */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader>
//           <div className="flex justify-between items-center">
//             <div>
//               <CardTitle className="text-white">Histórico de Trades Reais</CardTitle>
//               <CardDescription className="text-slate-400">
//                 Dados reais da sua conta Binance - {trades.length} trades encontrados
//               </CardDescription>
//             </div>
//             <div className="flex gap-2">
//               <Button
//                 onClick={fetchRealTrades}
//                 variant="outline"
//                 size="sm"
//                 disabled={isRefreshing}
//                 className="bg-transparent"
//               >
//                 <RefreshCw className={`w-4 h-4 ${isRefreshing ? "animate-spin" : ""}`} />
//                 Atualizar
//               </Button>
//               <Button onClick={exportTrades} variant="outline" size="sm" className="bg-transparent">
//                 <Download className="w-4 h-4" />
//                 Exportar
//               </Button>
//             </div>
//           </div>
//         </CardHeader>
//         <CardContent>
//           {/* Filtros */}
//           <div className="flex flex-wrap gap-4 mb-6">
//             <Input
//               placeholder="Buscar por símbolo ou ID..."
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
//               className="max-w-xs bg-slate-700 border-slate-600 text-white"
//             />

//             <Select value={filterSymbol} onValueChange={setFilterSymbol}>
//               <SelectTrigger className="w-40 bg-slate-700 border-slate-600 text-white">
//                 <SelectValue placeholder="Símbolo" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="all">Todos</SelectItem>
//                 {uniqueSymbols.map((symbol) => (
//                   <SelectItem key={symbol} value={symbol}>
//                     {symbol}
//                   </SelectItem>
//                 ))}
//               </SelectContent>
//             </Select>

//             <Select value={filterSide} onValueChange={setFilterSide}>
//               <SelectTrigger className="w-32 bg-slate-700 border-slate-600 text-white">
//                 <SelectValue placeholder="Lado" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="all">Todos</SelectItem>
//                 <SelectItem value="BUY">Compra</SelectItem>
//                 <SelectItem value="SELL">Venda</SelectItem>
//               </SelectContent>
//             </Select>
//           </div>

//           {/* Tabela */}
//           <div className="rounded-md border border-slate-700">
//             <Table>
//               <TableHeader>
//                 <TableRow className="border-slate-700">
//                   <TableHead className="text-slate-200">ID</TableHead>
//                   <TableHead className="text-slate-200">Símbolo</TableHead>
//                   <TableHead className="text-slate-200">Lado</TableHead>
//                   <TableHead className="text-slate-200">Quantidade</TableHead>
//                   <TableHead className="text-slate-200">Preço</TableHead>
//                   <TableHead className="text-slate-200">Total</TableHead>
//                   <TableHead className="text-slate-200">Comissão</TableHead>
//                   <TableHead className="text-slate-200">Data</TableHead>
//                 </TableRow>
//               </TableHeader>
//               <TableBody>
//                 {filteredTrades.map((trade) => (
//                   <TableRow key={trade.id} className="border-slate-700">
//                     <TableCell className="text-slate-300 font-mono text-xs">{trade.id.substring(0, 8)}...</TableCell>
//                     <TableCell className="text-slate-300 font-medium">{trade.symbol}</TableCell>
//                     <TableCell>
//                       <Badge variant={trade.side === "BUY" ? "default" : "destructive"}>{trade.side}</Badge>
//                     </TableCell>
//                     <TableCell className="text-slate-300">{trade.quantity}</TableCell>
//                     <TableCell className="text-slate-300">${trade.price.toFixed(8)}</TableCell>
//                     <TableCell className="text-slate-300">${trade.quoteQty.toFixed(2)}</TableCell>
//                     <TableCell className="text-slate-300">
//                       {trade.commission.toFixed(8)} {trade.commissionAsset}
//                     </TableCell>
//                     <TableCell className="text-slate-300">{new Date(trade.time).toLocaleString()}</TableCell>
//                   </TableRow>
//                 ))}
//               </TableBody>
//             </Table>
//           </div>

//           {filteredTrades.length === 0 && (
//             <div className="text-center py-8 text-slate-400">
//               {trades.length === 0
//                 ? "Nenhum trade encontrado na sua conta"
//                 : "Nenhum trade encontrado com os filtros aplicados"}
//             </div>
//           )}
//         </CardContent>
//       </Card>
//     </div>
//   )
// }









// "use client"

// import { useEffect, useState } from "react"
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// import { Badge } from "@/components/ui/badge"
// import { Loader2, RefreshCw, ExternalLink } from "lucide-react"
// import { Button } from "@/components/ui/button"

// interface Trade {
//   id: string
//   symbol: string
//   side: string
//   quantity: number
//   price: number
//   quoteQty: number
//   commission: number
//   commissionAsset: string
//   time: number
// }

// export function RealTradeHistory() {
//   const [trades, setTrades] = useState<Trade[]>([])
//   const [isLoading, setIsLoading] = useState(true)
//   const [stats, setStats] = useState({ totalTrades: 0, totalCommission: 0 })

//   const fetchHistory = async () => {
//     setIsLoading(true)
//     try {
//       const response = await fetch("/api/binance/trade-history")
//       if (!response.ok) throw new Error("Falha ao buscar histórico")
//       const data = await response.json()
//       if (data.success) {
//         setTrades(data.trades || [])
//         setStats(data.stats || { totalTrades: 0, totalCommission: 0 })
//       }
//     } catch (err) {
//       console.error(err)
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   useEffect(() => {
//     fetchHistory()
//   }, [])

//   const formatDate = (timestamp: number) => {
//     return new Date(timestamp).toLocaleString('pt-BR', {
//       day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
//     })
//   }

//   return (
//     <div className="space-y-6">
//       {/* Cards de Resumo */}
//       <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
//         <Card className="bg-slate-800 border-slate-700">
//           <CardContent className="pt-6">
//             <div className="text-2xl font-bold text-white">{stats.totalTrades}</div>
//             <p className="text-xs text-slate-400">Total de Trades</p>
//           </CardContent>
//         </Card>
//         <Card className="bg-slate-800 border-slate-700">
//           <CardContent className="pt-6">
//             <div className="text-2xl font-bold text-red-400">
//               ${stats.totalCommission.toFixed(4)}
//             </div>
//             <p className="text-xs text-slate-400">Taxas Pagas (Est. USDT)</p>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Tabela */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader className="flex flex-row items-center justify-between">
//           <CardTitle className="text-white">Histórico de Execuções</CardTitle>
//           <Button variant="ghost" size="sm" onClick={fetchHistory} disabled={isLoading}>
//             <RefreshCw className={`h-4 w-4 text-slate-400 ${isLoading ? "animate-spin" : ""}`} />
//           </Button>
//         </CardHeader>
//         <CardContent>
//           {isLoading && trades.length === 0 ? (
//             <div className="flex justify-center p-8"><Loader2 className="animate-spin text-blue-500" /></div>
//           ) : trades.length === 0 ? (
//             <div className="text-center py-8 text-slate-400">Nenhum trade recente encontrado.</div>
//           ) : (
//             <div className="overflow-x-auto">
//               <Table>
//                 <TableHeader>
//                   <TableRow className="border-slate-700 hover:bg-slate-800">
//                     <TableHead className="text-slate-400">Data/Hora</TableHead>
//                     <TableHead className="text-slate-400">Par</TableHead>
//                     <TableHead className="text-slate-400">Lado</TableHead>
//                     <TableHead className="text-slate-400 text-right">Preço</TableHead>
//                     <TableHead className="text-slate-400 text-right">Qtd</TableHead>
//                     <TableHead className="text-slate-400 text-right">Total ($)</TableHead>
//                     <TableHead className="text-slate-400 text-right">Taxa</TableHead>
//                   </TableRow>
//                 </TableHeader>
//                 <TableBody>
//                   {trades.map((trade) => (
//                     <TableRow key={trade.id} className="border-slate-700 hover:bg-slate-700/50">
//                       <TableCell className="text-slate-300 text-xs font-mono">
//                         {formatDate(trade.time)}
//                       </TableCell>
//                       <TableCell className="font-bold text-white">{trade.symbol}</TableCell>
//                       <TableCell>
//                         <Badge variant={trade.side === 'BUY' ? "default" : "destructive"} 
//                                className={trade.side === 'BUY' ? "bg-green-600" : "bg-red-600"}>
//                           {trade.side === 'BUY' ? 'COMPRA' : 'VENDA'}
//                         </Badge>
//                       </TableCell>
//                       <TableCell className="text-right text-slate-300">
//                         ${trade.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}
//                       </TableCell>
//                       <TableCell className="text-right text-slate-300">
//                         {trade.quantity}
//                       </TableCell>
//                       <TableCell className="text-right text-slate-200 font-medium">
//                         ${trade.quoteQty.toFixed(2)}
//                       </TableCell>
//                       <TableCell className="text-right text-xs text-slate-400">
//                         {trade.commission.toFixed(5)} {trade.commissionAsset}
//                       </TableCell>
//                     </TableRow>
//                   ))}
//                 </TableBody>
//               </Table>
//             </div>
//           )}
//         </CardContent>
//       </Card>
//     </div>
//   )
// }







// "use client"

// import { useState, useEffect } from "react"
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// import { Badge } from "@/components/ui/badge"
// import { Button } from "@/components/ui/button"
// import { Input } from "@/components/ui/input"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// import { Download, Filter, TrendingUp, RefreshCw, DollarSign, History } from "lucide-react"

// interface RealTrade {
//   id: string
//   symbol: string
//   side: "BUY" | "SELL"
//   quantity: number
//   price: number
//   quoteQty: number // Total gasto/recebido em USDT
//   commission: number
//   commissionAsset: string
//   time: number
// }

// export function RealTradeHistory() {
//   const [trades, setTrades] = useState<RealTrade[]>([])
//   const [filteredTrades, setFilteredTrades] = useState<RealTrade[]>([])
//   const [filterSymbol, setFilterSymbol] = useState("all")
//   const [filterType, setFilterType] = useState("all")
//   const [searchTerm, setSearchTerm] = useState("")
//   const [isLoading, setIsLoading] = useState(true)
//   const [stats, setStats] = useState({ totalTrades: 0, totalVolume: 0, totalFees: 0 })

//   const fetchHistory = async () => {
//     setIsLoading(true)
//     try {
//       const response = await fetch("/api/binance/trade-history")
//       if (!response.ok) throw new Error("Erro ao buscar histórico")
//       const data = await response.json()
      
//       if (data.success) {
//         const history = data.trades || []
//         setTrades(history)
//         setFilteredTrades(history)
        
//         // Calcula estatísticas REAIS
//         const fees = history.reduce((acc: number, t: RealTrade) => acc + (t.commissionAsset === 'USDT' ? t.commission : 0), 0)
//         const vol = history.reduce((acc: number, t: RealTrade) => acc + t.quoteQty, 0)
        
//         setStats({
//             totalTrades: history.length,
//             totalVolume: vol,
//             totalFees: fees
//         })
//       }
//     } catch (error) {
//       console.error("Erro:", error)
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   useEffect(() => {
//     fetchHistory()
//   }, [])

//   // Lógica de Filtro (Client-Side para rapidez)
//   useEffect(() => {
//     let filtered = trades

//     if (filterSymbol !== "all") {
//       filtered = filtered.filter((trade) => trade.symbol === filterSymbol)
//     }
//     if (filterType !== "all") {
//       filtered = filtered.filter((trade) => trade.side === filterType)
//     }
//     if (searchTerm) {
//       filtered = filtered.filter(
//         (trade) => trade.symbol.toLowerCase().includes(searchTerm.toLowerCase()) || trade.id.includes(searchTerm),
//       )
//     }
//     setFilteredTrades(filtered)
//   }, [trades, filterSymbol, filterType, searchTerm])

//   const exportTrades = () => {
//     const csvContent = [
//       ["ID", "Data", "Par", "Tipo", "Preço", "Qtd", "Total ($)", "Taxa"],
//       ...filteredTrades.map((t) => [
//         t.id,
//         new Date(t.time).toLocaleString(),
//         t.symbol,
//         t.side,
//         t.price,
//         t.quantity,
//         t.quoteQty,
//         `${t.commission} ${t.commissionAsset}`
//       ]),
//     ].map((row) => row.join(",")).join("\n")

//     const blob = new Blob([csvContent], { type: "text/csv" })
//     const url = window.URL.createObjectURL(blob)
//     const a = document.createElement("a")
//     a.href = url
//     a.download = "historico_binance_real.csv"
//     a.click()
//   }

//   const formatDate = (ts: number) => new Date(ts).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute:'2-digit'})

//   return (
//     <div className="space-y-6">
//       {/* Cards de Estatísticas REAIS */}
//       <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Volume Movimentado</CardTitle>
//             <TrendingUp className="h-4 w-4 text-green-500" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-white">${stats.totalVolume.toLocaleString(undefined, {maximumFractionDigits:0})}</div>
//             <p className="text-xs text-slate-400">Soma total (Compra + Venda)</p>
//           </CardContent>
//         </Card>

//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Taxas Pagas (Est.)</CardTitle>
//             <DollarSign className="h-4 w-4 text-red-400" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-slate-200">${stats.totalFees.toFixed(4)}</div>
//             <p className="text-xs text-slate-400">Em USDT (aprox.)</p>
//           </CardContent>
//         </Card>

//         <Card className="bg-slate-800 border-slate-700">
//           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
//             <CardTitle className="text-sm font-medium text-slate-200">Total de Trades</CardTitle>
//             <History className="h-4 w-4 text-blue-500" />
//           </CardHeader>
//           <CardContent>
//             <div className="text-2xl font-bold text-white">{stats.totalTrades}</div>
//             <p className="text-xs text-slate-400">Operações carregadas</p>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Painel Principal de Histórico */}
//       <Card className="bg-slate-800 border-slate-700">
//         <CardHeader>
//           <div className="flex justify-between items-center">
//             <div>
//               <CardTitle className="text-white">Histórico de Execuções</CardTitle>
//               <CardDescription className="text-slate-400">Dados oficiais da sua conta Binance</CardDescription>
//             </div>
//             <div className="flex gap-2">
//                 <Button variant="ghost" size="icon" onClick={fetchHistory} title="Atualizar">
//                     <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
//                 </Button>
//                 <Button onClick={exportTrades} variant="outline" className="flex items-center gap-2 bg-transparent">
//                 <Download className="w-4 h-4" />
//                 CSV
//                 </Button>
//             </div>
//           </div>
//         </CardHeader>
//         <CardContent>
//           {/* Filtros */}
//           <div className="flex flex-wrap gap-4 mb-6">
//             <Input
//               placeholder="Buscar símbolo..."
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
//               className="max-w-xs bg-slate-700 border-slate-600 text-white"
//             />
//             <Select value={filterType} onValueChange={setFilterType}>
//               <SelectTrigger className="w-32 bg-slate-700 border-slate-600 text-white">
//                 <SelectValue placeholder="Tipo" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="all">Todos</SelectItem>
//                 <SelectItem value="BUY">Compra</SelectItem>
//                 <SelectItem value="SELL">Venda</SelectItem>
//               </SelectContent>
//             </Select>
//           </div>

//           {/* Tabela Rica */}
//           <div className="rounded-md border border-slate-700">
//             <Table>
//               <TableHeader>
//                 <TableRow className="border-slate-700">
//                   <TableHead className="text-slate-200">Data/Hora</TableHead>
//                   <TableHead className="text-slate-200">Par</TableHead>
//                   <TableHead className="text-slate-200">Tipo</TableHead>
//                   <TableHead className="text-slate-200 text-right">Preço</TableHead>
//                   <TableHead className="text-slate-200 text-right">Qtd</TableHead>
//                   <TableHead className="text-slate-200 text-right">Total (USDT)</TableHead>
//                   <TableHead className="text-slate-200 text-right">Taxa</TableHead>
//                 </TableRow>
//               </TableHeader>
//               <TableBody>
//                 {filteredTrades.map((trade) => (
//                   <TableRow key={trade.id} className="border-slate-700 hover:bg-slate-700/50">
//                     <TableCell className="text-slate-300 text-xs font-mono">{formatDate(trade.time)}</TableCell>
//                     <TableCell className="text-slate-200 font-bold">{trade.symbol}</TableCell>
//                     <TableCell>
//                       <Badge variant="outline" className={trade.side === "BUY" ? "text-green-400 border-green-900 bg-green-900/20" : "text-red-400 border-red-900 bg-red-900/20"}>
//                         {trade.side === "BUY" ? "COMPRA" : "VENDA"}
//                       </Badge>
//                     </TableCell>
//                     <TableCell className="text-slate-300 text-right font-mono">${trade.price.toLocaleString()}</TableCell>
//                     <TableCell className="text-slate-400 text-right font-mono text-xs">{trade.quantity}</TableCell>
//                     <TableCell className="text-yellow-500 text-right font-medium font-mono">${trade.quoteQty.toFixed(2)}</TableCell>
//                     <TableCell className="text-red-300 text-right text-xs font-mono">
//                       {trade.commission.toFixed(5)} {trade.commissionAsset}
//                     </TableCell>
//                   </TableRow>
//                 ))}
//               </TableBody>
//             </Table>
//           </div>
//         </CardContent>
//       </Card>
//     </div>
//   )
// }






// ULTIMO FUNCIONANDO MAS ESTA COM ALGUNS BUGS

"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Download, Filter, TrendingUp, RefreshCw, DollarSign, History } from "lucide-react"

// Interface para Trades Reais
interface RealTrade {
  id: string
  symbol: string
  side: "BUY" | "SELL"
  quantity: number
  price: number
  quoteQty: number // Total gasto/recebido em USDT
  commission: number
  commissionAsset: string
  time: number
}

export function RealTradeHistory() {
  const [trades, setTrades] = useState<RealTrade[]>([])
  const [filteredTrades, setFilteredTrades] = useState<RealTrade[]>([])
  const [filterSymbol, setFilterSymbol] = useState("all")
  const [filterType, setFilterType] = useState("all")
  const [searchTerm, setSearchTerm] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [stats, setStats] = useState({ totalTrades: 0, totalVolume: 0, totalFees: 0 })

  // Busca histórico REAL
  const fetchHistory = async () => {
    setIsLoading(true)
    try {
      const response = await fetch("/api/binance/trade-history")
      if (!response.ok) throw new Error("Erro ao buscar histórico")
      const data = await response.json()
      
      if (data.success) {
        const history = data.trades || []
        setTrades(history)
        setFilteredTrades(history)
        
        // Calcula estatísticas baseadas nos dados REAIS
        const fees = history.reduce((acc: number, t: RealTrade) => acc + (t.commissionAsset === 'USDT' ? t.commission : 0), 0)
        const vol = history.reduce((acc: number, t: RealTrade) => acc + t.quoteQty, 0)
        
        setStats({
            totalTrades: history.length,
            totalVolume: vol,
            totalFees: fees
        })
      }
    } catch (error) {
      console.error("Erro:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  // Lógica de Filtro
  useEffect(() => {
    let filtered = trades

    if (filterSymbol !== "all") {
      filtered = filtered.filter((trade) => trade.symbol === filterSymbol)
    }
    if (filterType !== "all") {
      filtered = filtered.filter((trade) => trade.side === filterType)
    }
    if (searchTerm) {
      filtered = filtered.filter(
        (trade) => trade.symbol.toLowerCase().includes(searchTerm.toLowerCase()) || trade.id.includes(searchTerm),
      )
    }
    setFilteredTrades(filtered)
  }, [trades, filterSymbol, filterType, searchTerm])

  const exportTrades = () => {
    const csvContent = [
      ["ID", "Data", "Par", "Tipo", "Preço", "Qtd", "Total ($)", "Taxa"],
      ...filteredTrades.map((t) => [
        t.id,
        new Date(t.time).toLocaleString(),
        t.symbol,
        t.side,
        t.price,
        t.quantity,
        t.quoteQty,
        `${t.commission} ${t.commissionAsset}`
      ]),
    ].map((row) => row.join(",")).join("\n")

    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "historico_binance_real.csv"
    a.click()
  }

  const formatDate = (ts: number) => new Date(ts).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute:'2-digit'})

  return (
    <div className="space-y-6">
      {/* Cards de Estatísticas (Calculadas do Real) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Volume Movimentado</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">${stats.totalVolume.toLocaleString(undefined, {maximumFractionDigits:0})}</div>
            <p className="text-xs text-slate-400">Soma total (Compra + Venda)</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Taxas Pagas (Est.)</CardTitle>
            <DollarSign className="h-4 w-4 text-red-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-200">${stats.totalFees.toFixed(4)}</div>
            <p className="text-xs text-slate-400">Em USDT (aprox.)</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Total de Trades</CardTitle>
            <History className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{stats.totalTrades}</div>
            <p className="text-xs text-slate-400">Operações carregadas</p>
          </CardContent>
        </Card>
      </div>

      {/* Painel Principal de Histórico */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-white">Histórico de Execuções</CardTitle>
              <CardDescription className="text-slate-400">Dados oficiais da sua conta Binance</CardDescription>
            </div>
            <div className="flex gap-2">
                <Button variant="ghost" size="icon" onClick={fetchHistory} title="Atualizar">
                    <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                </Button>
                <Button onClick={exportTrades} variant="outline" className="flex items-center gap-2 bg-transparent">
                <Download className="w-4 h-4" />
                CSV
                </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Filtros */}
          <div className="flex flex-wrap gap-4 mb-6">
            <Input
              placeholder="Buscar símbolo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-xs bg-slate-700 border-slate-600 text-white"
            />
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-32 bg-slate-700 border-slate-600 text-white">
                <SelectValue placeholder="Tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos</SelectItem>
                <SelectItem value="BUY">Compra</SelectItem>
                <SelectItem value="SELL">Venda</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Tabela Rica */}
          <div className="rounded-md border border-slate-700">
            <Table>
              <TableHeader>
                <TableRow className="border-slate-700">
                  <TableHead className="text-slate-200">Data/Hora</TableHead>
                  <TableHead className="text-slate-200">Par</TableHead>
                  <TableHead className="text-slate-200">Tipo</TableHead>
                  <TableHead className="text-slate-200 text-right">Preço</TableHead>
                  <TableHead className="text-slate-200 text-right">Qtd</TableHead>
                  <TableHead className="text-slate-200 text-right">Total (USDT)</TableHead>
                  <TableHead className="text-slate-200 text-right">Taxa</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTrades.map((trade) => (
                  <TableRow key={trade.id} className="border-slate-700 hover:bg-slate-700/50">
                    <TableCell className="text-slate-300 text-xs font-mono">{formatDate(trade.time)}</TableCell>
                    <TableCell className="text-slate-200 font-bold">{trade.symbol}</TableCell>
                    <TableCell>
                      <Badge variant="outline" className={trade.side === "BUY" ? "text-green-400 border-green-900 bg-green-900/20" : "text-red-400 border-red-900 bg-red-900/20"}>
                        {trade.side === "BUY" ? "COMPRA" : "VENDA"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-slate-300 text-right font-mono">${trade.price.toLocaleString()}</TableCell>
                    <TableCell className="text-slate-400 text-right font-mono text-xs">{trade.quantity}</TableCell>
                    <TableCell className="text-yellow-500 text-right font-medium font-mono">${trade.quoteQty.toFixed(2)}</TableCell>
                    <TableCell className="text-red-300 text-right text-xs font-mono">
                      {trade.commission.toFixed(5)} {trade.commissionAsset}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
          {filteredTrades.length === 0 && !isLoading && (
            <div className="text-center py-8 text-slate-400">Nenhum trade encontrado.</div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}







