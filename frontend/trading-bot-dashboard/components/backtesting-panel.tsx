"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Loader2, PlayCircle, TrendingUp, TrendingDown, Activity } from "lucide-react"
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { useToast } from "@/components/ui/use-toast"

export function BacktestingPanel() {
  const [availableSymbols, setAvailableSymbols] = useState<string[]>([])
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>([]) 
  const [testPeriod, setTestPeriod] = useState("30")
  const [useMacro, setUseMacro] = useState(false) 
  const [initialCapital, setInitialCapital] = useState("10000") 
  
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const { toast } = useToast()

  useEffect(() => {
    fetch('/api/symbols')
      .then(res => res.json())
      .then(data => {
        setAvailableSymbols(data)
        if (data.length > 0) setSelectedSymbols([data[0]])
      })
      .catch(() => toast({ title: "Erro", description: "Falha ao carregar ativos" }))
  }, [])

  const toggleSymbol = (sym: string) => {
    if (selectedSymbols.includes(sym)) {
      setSelectedSymbols(selectedSymbols.filter(s => s !== sym))
    } else {
      if (selectedSymbols.length >= 5) {
        toast({ title: "Limite", description: "Máximo de 5 ativos por vez.", variant: "destructive" })
        return
      }
      setSelectedSymbols([...selectedSymbols, sym])
    }
  }

  const runBacktest = async () => {
    if (selectedSymbols.length === 0) {
        toast({ title: "Atenção", description: "Selecione pelo menos um ativo." })
        return
    }
    
    setIsRunning(true)
    setResults(null)

    try {
      const response = await fetch('/api/backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            symbols: selectedSymbols, 
            period: parseInt(testPeriod),
            use_macro_regime: useMacro,
            initial_capital: parseFloat(initialCapital)
        })
      })
      
      const data = await response.json()
      if (response.ok) {
        setResults(data)
        toast({ title: "Sucesso", description: `Backtest concluído.` })
      } else {
        throw new Error(data.error)
      }
    } catch (error: any) {
      toast({ title: "Erro", description: error.message, variant: "destructive" })
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
          Simule sua estratégia com capital personalizado.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6">
          
          <div className="flex flex-wrap items-end gap-6 p-4 bg-slate-900/50 rounded-lg border border-slate-700">
            <div className="space-y-2">
                <Label className="text-white">Ativos ({selectedSymbols.length}/5)</Label>
                <div className="h-32 w-[200px] overflow-y-auto border border-slate-600 rounded bg-slate-800 p-2 space-y-2">
                    {availableSymbols.map(sym => (
                        <div key={sym} className="flex items-center space-x-2">
                            <Checkbox 
                                id={sym} 
                                checked={selectedSymbols.includes(sym)}
                                onCheckedChange={() => toggleSymbol(sym)}
                                className="border-slate-500 data-[state=checked]:bg-blue-600"
                            />
                            <label htmlFor={sym} className="text-sm text-slate-300 cursor-pointer">{sym}</label>
                        </div>
                    ))}
                </div>
            </div>

            <div className="space-y-2">
                <Label className="text-white">Período</Label>
                <Select value={testPeriod} onValueChange={setTestPeriod}>
                    <SelectTrigger className="w-[140px] bg-slate-700 border-slate-600 text-white"><SelectValue /></SelectTrigger>
                    <SelectContent className="bg-slate-700 border-slate-600 text-white">
                        <SelectItem value="30">30 Dias</SelectItem>
                        <SelectItem value="60">60 Dias</SelectItem>
                        <SelectItem value="180">180 Dias</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            <div className="space-y-2">
                <Label htmlFor="capital" className="text-white">Capital Inicial ($)</Label>
                <Input 
                    id="capital" 
                    type="number" 
                    value={initialCapital} 
                    onChange={(e) => setInitialCapital(e.target.value)}
                    className="w-[140px] bg-slate-700 border-slate-600 text-white"
                />
            </div>

            <div className="flex items-center gap-2 pb-2">
                <Switch checked={useMacro} onCheckedChange={setUseMacro} id="macro-mode" />
                <Label htmlFor="macro-mode" className="text-white cursor-pointer">Usar Filtro Macro</Label>
            </div>

            <Button onClick={runBacktest} disabled={isRunning} className="bg-blue-600 hover:bg-blue-700 text-white mb-1">
              {isRunning ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <PlayCircle className="mr-2 h-4 w-4" />}
              Rodar
            </Button>
          </div>

          {results && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Lucro Total Portfolio</div>
                  <div className={`text-2xl font-bold ${results.total_pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    ${results.total_pnl}
                  </div>
                </div>
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Saldo Final</div>
                  <div className="text-2xl font-bold text-white">${results.final_balance}</div>
                </div>
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Win Rate Médio</div>
                  <div className="text-2xl font-bold text-white">{results.win_rate}%</div>
                </div>
                <div className="p-4 border border-slate-700 rounded-lg bg-slate-900/50">
                  <div className="text-sm text-slate-400">Total Trades</div>
                  <div className="text-2xl font-bold text-white">{results.total_trades}</div>
                </div>
              </div>

              <div className="h-[250px] w-full border border-slate-700 rounded-lg p-4 bg-slate-900/50">
                <h4 className="mb-2 text-sm font-medium text-slate-200">Curva de Patrimônio (Soma)</h4>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={results.equity_curve}>
                    <defs>
                      <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.5} />
                    <XAxis dataKey="time" hide />
                    <YAxis domain={['auto', 'auto']} stroke="#9CA3AF" />
                    <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', color: '#fff' }}/>
                    <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="url(#colorTotal)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">Detalhes por Ativo</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {results.details?.map((item: any) => (
                        <Card key={item.symbol} className="bg-slate-800 border-slate-600">
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-center">
                                    <CardTitle className="text-base text-white">{item.symbol}</CardTitle>
                                    {item.regime === "BULLISH" ? 
                                        <TrendingUp className="text-green-500 h-4 w-4" /> : 
                                        <TrendingDown className="text-red-500 h-4 w-4" />
                                    }
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="flex justify-between mb-2">
                                    <span className="text-sm text-slate-400">P&L:</span>
                                    <span className={`font-bold ${item.pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>${item.pnl}</span>
                                </div>
                                <div className="flex justify-between mb-4">
                                    <span className="text-sm text-slate-400">Trades:</span>
                                    <span className="text-white">{item.total_trades}</span>
                                </div>
                                <div className="h-[60px] w-full">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <AreaChart data={item.equity_curve}>
                                            <Area type="monotone" dataKey="value" stroke="#10b981" fill="none" strokeWidth={2} />
                                        </AreaChart>
                                    </ResponsiveContainer>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}