"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Shield, AlertTriangle, TrendingDown, TrendingUp, Settings2, Wallet, DollarSign, Activity } from "lucide-react"
import { useToast } from "@/components/ui/use-toast"

export function RiskManagement() {
  // --- Estados Gerais e de Estratégia ---
  const [useMacroRegime, setUseMacroRegime] = useState(true)
  const [balance, setBalance] = useState(0.0) 
  const [tradeAmount, setTradeAmount] = useState(10.0) 
  
  // --- Estados de Gestão de Risco (Arrays para Sliders) ---
  const [stopLossEnabled, setStopLossEnabled] = useState(true)
  const [takeProfitEnabled, setTakeProfitEnabled] = useState(true)
  const [stopLossPercent, setStopLossPercent] = useState([2.0])
  const [takeProfitPercent, setTakeProfitPercent] = useState([5.0])
  const [maxPositionSize, setMaxPositionSize] = useState([10])
  const [maxDailyLoss, setMaxDailyLoss] = useState(500)
  const [maxOpenPositions, setMaxOpenPositions] = useState(3)
  const [riskPerTrade, setRiskPerTrade] = useState([1.0])
  
  // --- Estados Visuais (Status) ---
  const [openPositionsCount, setOpenPositionsCount] = useState(0)
  const [totalExposure, setTotalExposure] = useState(0)

  const { toast } = useToast()

  // Carrega dados do servidor ao abrir a tela
  useEffect(() => {
    // 1. Saldo
    fetch("/api/balance")
        .then(res => res.json())
        .then(data => setBalance(data.balance))
        .catch(err => console.error("Erro saldo:", err))

    // 2. Configurações Salvas
    fetch("/api/risk-settings")
      .then((res) => res.json())
      .then((data) => {
        if (data) {
          if (data.use_macro_regime !== undefined) setUseMacroRegime(data.use_macro_regime)
          if (data.tradeAmount) setTradeAmount(data.tradeAmount)
          
          if (data.stopLoss) { 
            setStopLossEnabled(data.stopLoss.enabled)
            setStopLossPercent([data.stopLoss.percent]) 
          }
          if (data.takeProfit) { 
            setTakeProfitEnabled(data.takeProfit.enabled)
            setTakeProfitPercent([data.takeProfit.percent]) 
          }
          if (data.maxPositionSize) setMaxPositionSize([data.maxPositionSize])
          if (data.maxDailyLoss) setMaxDailyLoss(data.maxDailyLoss)
          if (data.maxOpenPositions) setMaxOpenPositions(data.maxOpenPositions)
          if (data.riskPerTrade) setRiskPerTrade([data.riskPerTrade])
        }
      })
      .catch((err) => console.error("Erro configs:", err))

    // 3. Status Atual
    fetch("/api/bot/status").then(res => res.json()).then(data => {
        if(data.positions) {
            const pos = Object.values(data.positions)
            setOpenPositionsCount(pos.length)
            setTotalExposure(pos.length * 10) // Estimativa visual
        }
    }).catch(console.error)
  }, [])

  const handleSaveSettings = async () => {
    const settings = {
      use_macro_regime: useMacroRegime,
      tradeAmount: tradeAmount,
      stopLoss: { enabled: stopLossEnabled, percent: stopLossPercent[0] },
      takeProfit: { enabled: takeProfitEnabled, percent: takeProfitPercent[0] },
      maxPositionSize: maxPositionSize[0],
      maxDailyLoss: maxDailyLoss,
      maxOpenPositions: maxOpenPositions,
      riskPerTrade: riskPerTrade[0],
    }

    try {
      const response = await fetch("/api/risk-settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      })

      if (response.ok) {
        toast({ 
            title: "Sucesso!", 
            description: "Configurações salvas e aplicadas ao robô.", 
            className: "bg-green-600 text-white border-none" 
        })
      } else {
        toast({ title: "Erro", description: "Falha ao salvar.", variant: "destructive" })
      }
    } catch (error) {
      toast({ title: "Erro", description: "Erro de conexão.", variant: "destructive" })
    }
  }

  return (
    <div className="space-y-6">
      
      {/* 1. Saldo e Valor da Ordem */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                    <Wallet className="w-5 h-5 text-green-400"/> Carteira Binance
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="text-3xl font-bold text-white">
                    {balance.toLocaleString('en-US', { style: 'currency', currency: 'USD' })}
                </div>
                <p className="text-sm text-slate-400">Saldo disponível em USDT</p>
            </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700 border-l-4 border-l-green-500">
            <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                    <DollarSign className="w-5 h-5"/> Valor da Operação
                </CardTitle>
                <CardDescription className="text-slate-400">
                    Quanto comprar em cada trade?
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="relative">
                    <span className="absolute left-3 top-2.5 text-slate-400">USDT</span>
                    <Input 
                        type="number" 
                        value={tradeAmount} 
                        onChange={(e) => setTradeAmount(parseFloat(e.target.value))}
                        className="bg-slate-900 border-slate-600 text-white pl-16 text-lg font-bold"
                    />
                </div>
                <p className="text-xs text-slate-400 mt-2">
                    O robô usará este valor fixo para cada compra.
                </p>
            </CardContent>
        </Card>
      </div>

      {/* 2. Estratégia Global */}
      <Card className="bg-slate-800 border-slate-700 border-l-4 border-l-blue-500">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-white">
            <Settings2 className="w-5 h-5" /> Filtros de Mercado
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between p-4 bg-slate-900/50 rounded-lg border border-slate-700">
            <div className="space-y-1">
              <Label className="text-white text-base">Filtro de Regime Macro</Label>
              <p className="text-sm text-slate-400">Só compra se Preço &gt; EMA 50 (Diário).</p>
            </div>
            <Switch 
                checked={useMacroRegime} 
                onCheckedChange={setUseMacroRegime} 
                className="data-[state=checked]:bg-green-500" 
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* 3. Stop Loss & Take Profit (Visual Rico Restaurado) */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Shield className="w-5 h-5" /> Stop Loss & Take Profit
            </CardTitle>
            <CardDescription className="text-slate-400">Limites automáticos de proteção.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            
            {/* Stop Loss */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                        <Label className="text-slate-200">Stop Loss Automático</Label>
                        <p className="text-xs text-slate-400">Vender se cair X%</p>
                    </div>
                    <Switch checked={stopLossEnabled} onCheckedChange={setStopLossEnabled} />
                </div>
                
                {stopLossEnabled && (
                <div className="space-y-2 p-3 bg-slate-900/30 rounded-md border border-slate-700/50">
                    <div className="flex justify-between items-center mb-2">
                        <Label className="text-slate-300">Percentual de Perda</Label>
                        <span className="text-red-400 font-bold text-lg">{stopLossPercent[0]}%</span>
                    </div>
                    <Slider 
                        value={stopLossPercent} 
                        onValueChange={setStopLossPercent} 
                        max={10} min={0.5} step={0.1} 
                        className="w-full"
                    />
                    <div className="flex justify-between text-xs text-slate-500">
                        <span>0.5%</span>
                        <span>10%</span>
                    </div>
                </div>
                )}
            </div>

            <div className="h-[1px] bg-slate-700 w-full"></div>

            {/* Take Profit */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                        <Label className="text-slate-200">Take Profit Automático</Label>
                        <p className="text-xs text-slate-400">Vender se subir X%</p>
                    </div>
                    <Switch checked={takeProfitEnabled} onCheckedChange={setTakeProfitEnabled} />
                </div>
                
                {takeProfitEnabled && (
                <div className="space-y-2 p-3 bg-slate-900/30 rounded-md border border-slate-700/50">
                    <div className="flex justify-between items-center mb-2">
                        <Label className="text-slate-300">Percentual de Lucro</Label>
                        <span className="text-green-400 font-bold text-lg">{takeProfitPercent[0]}%</span>
                    </div>
                    <Slider 
                        value={takeProfitPercent} 
                        onValueChange={setTakeProfitPercent} 
                        max={20} min={1} step={0.5} 
                        className="w-full"
                    />
                    <div className="flex justify-between text-xs text-slate-500">
                        <span>1%</span>
                        <span>20%</span>
                    </div>
                </div>
                )}
            </div>
          </CardContent>
        </Card>

        {/* 4. Gestão de Posições (Visual Rico Restaurado) */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
                <TrendingUp className="w-5 h-5" /> Gestão de Tamanho
            </CardTitle>
            <CardDescription className="text-slate-400">Controle de exposição e risco.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            
            <div className="space-y-4 p-3 bg-slate-900/30 rounded-md border border-slate-700/50">
              <div className="flex justify-between items-center">
                <Label className="text-slate-200">Tamanho Máx. Posição (% Carteira)</Label>
                <span className="text-white font-bold">{maxPositionSize[0]}%</span>
              </div>
              <Slider 
                value={maxPositionSize} 
                onValueChange={setMaxPositionSize} 
                max={50} min={1} step={1} 
                className="w-full"
              />
            </div>

            <div className="space-y-4 p-3 bg-slate-900/30 rounded-md border border-slate-700/50">
              <div className="flex justify-between items-center">
                 <Label className="text-slate-200">Risco por Trade (% Carteira)</Label>
                 <span className="text-white font-bold">{riskPerTrade[0]}%</span>
              </div>
              <Slider 
                value={riskPerTrade} 
                onValueChange={setRiskPerTrade} 
                max={5} min={0.1} step={0.1} 
                className="w-full"
              />
            </div>

            <div className="space-y-2 pt-2">
              <Label className="text-slate-200">Máximo de Posições Simultâneas</Label>
              <Input 
                type="number" 
                value={maxOpenPositions} 
                onChange={(e) => setMaxOpenPositions(Number(e.target.value))} 
                className="bg-slate-700 text-white" 
                min={1} max={10} 
              />
            </div>

          </CardContent>
        </Card>
      </div>
      
      {/* 5. Limites de Segurança */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-white">
            <AlertTriangle className="w-5 h-5" /> Limites de Segurança
          </CardTitle>
          <CardDescription className="text-slate-400">Pausa automática em caso de perdas elevadas.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-200">Perda Máxima Diária ($)</Label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-slate-400">$</span>
                <Input 
                    type="number" 
                    value={maxDailyLoss} 
                    onChange={(e) => setMaxDailyLoss(Number(e.target.value))} 
                    className="bg-slate-700 text-white pl-6" 
                    min={0}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 6. Status em Tempo Real */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
                <Activity className="w-5 h-5" /> Status em Tempo Real
            </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-700 rounded-lg border border-slate-600">
                <div className="flex items-center gap-2 mb-2"><TrendingDown className="w-4 h-4 text-red-400" /><span className="text-slate-200">Perda Hoje</span></div>
                <div className="text-2xl font-bold text-white">$0.00</div>
            </div>
            <div className="p-4 bg-slate-700 rounded-lg border border-slate-600">
                <div className="flex items-center gap-2 mb-2"><Shield className="w-4 h-4 text-blue-400" /><span className="text-slate-200">Posições</span></div>
                <div className="text-2xl font-bold text-white">{openPositionsCount}</div>
            </div>
            <div className="p-4 bg-slate-700 rounded-lg border border-slate-600">
                <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-4 h-4 text-green-400" /><span className="text-slate-200">Exposição</span></div>
                <div className="text-2xl font-bold text-white">{totalExposure}%</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Button onClick={handleSaveSettings} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 text-lg shadow-lg shadow-blue-900/20">
        Salvar Todas as Configurações
      </Button>
    </div>
  )
}