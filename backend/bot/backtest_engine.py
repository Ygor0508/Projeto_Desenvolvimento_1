# # backend/bot/backtest_engine.py
# import pandas as pd
# import numpy as np
# from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
# from backend.bot.feature_engineering import (
#     add_advanced_technical_features, add_multitimeframe_features, 
#     create_labels_with_dynamic_risk, check_bullish_regime, is_trending_market
# )
# from backend.bot.training_manager import train_model_pipeline
# from backend.bot.data_handler import get_historical_data
# from backend.config import TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO
# from sklearn.preprocessing import StandardScaler
# from xgboost import XGBClassifier

# def run_dashboard_backtest(symbol, days=365):
#     """
#     Roda um backtest sob demanda para o Dashboard usando a Lógica de Produção v3.1.
#     """
#     print(f"Iniciando Backtest de Dashboard para {symbol}...")
    
#     # 1. Coleta de Dados
#     df_15m = get_historical_data(symbol, TIMEFRAME, days_back=days)
#     df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=days)
#     df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=days + 50) 
    
#     if df_15m is None or df_1h is None or df_1d is None:
#         return {"error": "Dados insuficientes ou falha na API Binance"}

#     # 2. Define Regime (Fase 0)
#     regime_bullish = check_bullish_regime(df_1d)
    
#     # 3. Prepara Dados e Treina Modelo (Simulação rápida)
#     df = add_advanced_technical_features(df_15m)
#     df = add_multitimeframe_features(df, df_1h)
    
#     model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
#     if not model:
#         return {"error": "Falha ao treinar modelo para backtest"}

#     # --- SIMULAÇÃO LOOP (Fases 1, 3 e 4) ---
#     # Testa nos últimos 20% dos dados para ser realista
#     test_size = int(len(df) * 0.2)
#     df_test = df.iloc[-test_size:].copy()
    
#     balance = 10000.0
#     position = None
#     trades = []
#     equity_curve = [] # Dados para o gráfico
    
#     X_test = df_test[ALL_FEATURES]
#     X_test_scaled = scaler.transform(X_test)
#     probs = model.predict_proba(X_test_scaled)[:, 1]
#     df_test['probability'] = probs
    
#     threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    
#     for i in range(len(df_test)):
#         row = df_test.iloc[i]
#         current_price = row['close']
#         timestamp = df_test.index[i]
#         atr = row['atr']
        
#         # Atualiza curva
#         current_equity = balance
#         if position:
#             pnl_open = (current_price - position['entry_price']) * position['size']
#             current_equity += pnl_open
#         equity_curve.append({'time': str(timestamp), 'value': current_equity})

#         if position is None:
#             # Entrada
#             if row['probability'] >= threshold: # 1. IA
#                 if regime_bullish:              # 2. Macro
#                     if is_trending_market(row): # 3. Local
#                         amount = balance 
#                         size = amount / current_price
#                         sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
#                         tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                        
#                         position = {
#                             'entry_price': current_price, 'size': size,
#                             'sl': sl, 'tp': tp, 'highest_price': current_price,
#                             'entry_time': str(timestamp)
#                         }
#                         balance = 0 
#         else:
#             # Saída
#             position['highest_price'] = max(position['highest_price'], current_price)
#             new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
#             position['sl'] = max(position['sl'], new_sl)
            
#             reason = None
#             if current_price >= position['tp']: reason = "TAKE_PROFIT"
#             elif current_price <= position['sl']: reason = "STOP_LOSS"
            
#             if reason:
#                 pnl = (current_price - position['entry_price']) * position['size']
#                 balance = (position['size'] * current_price)
#                 trades.append({
#                     'entry_date': position['entry_time'],
#                     'exit_date': str(timestamp),
#                     'pnl': pnl,
#                     'reason': reason
#                 })
#                 position = None

#     total_trades = len(trades)
#     wins = len([t for t in trades if t['pnl'] > 0])
#     win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
#     total_pnl = balance - 10000.0 if position is None else (balance + (position['size'] * df_test.iloc[-1]['close'])) - 10000.0

#     # Retorno JSON formatado para o Frontend
#     return {
#         "symbol": symbol,
#         "total_trades": total_trades,
#         "win_rate": round(win_rate, 2),
#         "total_pnl": round(total_pnl, 2),
#         "final_balance": round(10000.0 + total_pnl, 2),
#         "trades": trades,
#         "equity_curve": equity_curve,
#         "regime": "BULLISH" if regime_bullish else "BEARISH"
#     }




# #FUNCIOANNDO NORMALMENTE COM O REGIME MACRO, REGIME MUITO RIGIDO
# # backend/bot/backtest_engine.py
# import pandas as pd
# import numpy as np
# from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
# from backend.bot.feature_engineering import (
#     add_advanced_technical_features, add_multitimeframe_features, 
#     create_labels_with_dynamic_risk, check_bullish_regime, is_trending_market
# )
# from backend.bot.training_manager import train_model_pipeline
# from backend.bot.data_handler import get_historical_data
# from backend.config import TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO
# import backend.config as config
# from sklearn.preprocessing import StandardScaler
# from xgboost import XGBClassifier

# def run_dashboard_backtest(symbol, days=60): # Padrão reduzido para 60 dias para evitar travamento
#     """
#     Roda um backtest sob demanda para o Dashboard.
#     """
#     print(f"Iniciando Backtest de Dashboard para {symbol} ({days} dias)...")
    
#     # Validação de Segurança antes de começar
#     if not config.client:
#         print("ERRO: Cliente Binance não carregado no Backtest.")
#         return {"error": "Chaves da Binance não configuradas no Backend."}

#     # 1. Coleta de Dados (Limitada para performance)
#     # Se o usuário pedir muitos dias, limitamos para evitar timeout do navegador
#     safe_days = min(days, 180) 
    
#     try:
#         df_15m = get_historical_data(symbol, TIMEFRAME, days_back=safe_days)
#         df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=safe_days)
#         df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=safe_days + 50) 
        
#         if df_15m is None or df_15m.empty:
#             return {"error": f"Sem dados de 15m para {symbol}. Verifique se o ativo existe."}
            
#     except Exception as e:
#         return {"error": f"Erro na Binance: {str(e)}"}

#     # 2. Define Regime e Prepara Dados
#     regime_bullish = check_bullish_regime(df_1d)
    
#     df = add_advanced_technical_features(df_15m)
#     df = add_multitimeframe_features(df, df_1h)
    
#     # Treina modelo rápido
#     model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
#     if not model:
#         return {"error": "Dados insuficientes para gerar sinais de IA."}

#     # 3. Simulação
#     test_size = int(len(df) * 0.3) # Testa nos últimos 30%
#     df_test = df.iloc[-test_size:].copy()
    
#     if df_test.empty:
#         return {"error": "Dataset de teste vazio."}

#     balance = 10000.0
#     position = None
#     trades = []
#     equity_curve = []
    
#     # Predição em lote (Muito mais rápido)
#     try:
#         X_test = df_test[ALL_FEATURES]
#         X_test_scaled = scaler.transform(X_test)
#         probs = model.predict_proba(X_test_scaled)[:, 1]
#         df_test['probability'] = probs
#     except Exception as e:
#         return {"error": f"Erro na predição da IA: {str(e)}"}
    
#     threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    
#     for i in range(len(df_test)):
#         row = df_test.iloc[i]
#         current_price = row['close']
#         timestamp = df_test.index[i]
#         atr = row['atr']
        
#         # Log da curva (reduzido para não pesar o JSON)
#         # Só salva a cada 4 candles (1 hora)
#         if i % 4 == 0: 
#             current_equity = balance + ((current_price - position['entry_price']) * position['size'] if position else 0)
#             equity_curve.append({'time': str(timestamp), 'value': round(current_equity, 2)})

#         if position is None:
#             if row['probability'] >= threshold and regime_bullish and is_trending_market(row):
            
#                 amount = balance 
#                 size = amount / current_price
#                 sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
#                 tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                
#                 position = {
#                     'entry_price': current_price, 'size': size,
#                     'sl': sl, 'tp': tp, 'highest_price': current_price,
#                     'entry_time': str(timestamp)
#                 }
#                 balance = 0 
#         else:
#             position['highest_price'] = max(position['highest_price'], current_price)
#             new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
#             position['sl'] = max(position['sl'], new_sl)
            
#             reason = None
#             if current_price >= position['tp']: reason = "TAKE_PROFIT"
#             elif current_price <= position['sl']: reason = "STOP_LOSS"
            
#             if reason:
#                 pnl = (current_price - position['entry_price']) * position['size']
#                 balance = (position['size'] * current_price)
#                 trades.append({
#                     'entry_date': position['entry_time'],
#                     'exit_date': str(timestamp),
#                     'pnl': round(pnl, 2),
#                     'reason': reason
#                 })
#                 position = None

#     total_trades = len(trades)
#     wins = len([t for t in trades if t['pnl'] > 0])
#     win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
#     final_balance = balance if position is None else (balance + (position['size'] * df_test.iloc[-1]['close']))
#     total_pnl = final_balance - 10000.0

#     return {
#         "symbol": symbol,
#         "total_trades": total_trades,
#         "win_rate": round(win_rate, 2),
#         "total_pnl": round(total_pnl, 2),
#         "final_balance": round(final_balance, 2),
#         "trades": trades,
#         "equity_curve": equity_curve,
#         "regime": "BULLISH" if regime_bullish else "BEARISH"
#     }





# # SEM O REGIME MACRO, TESTE
# # backend/bot/backtest_engine.py
# import pandas as pd
# import numpy as np
# from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
# from backend.bot.feature_engineering import (
#     add_advanced_technical_features, add_multitimeframe_features, 
#     create_labels_with_dynamic_risk, check_bullish_regime, is_trending_market
# )
# from backend.bot.training_manager import train_model_pipeline
# from backend.bot.data_handler import get_historical_data
# from backend.config import TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO
# import backend.config as config
# from sklearn.preprocessing import StandardScaler
# from xgboost import XGBClassifier

# def run_dashboard_backtest(symbol, days=60): # Padrão reduzido para 60 dias para evitar travamento
#     """
#     Roda um backtest sob demanda para o Dashboard.
#     MODO TESTE: Filtro de Regime Macro IGNORADO na execução.
#     """
#     print(f"Iniciando Backtest de Dashboard para {symbol} ({days} dias)...")
    
#     # Validação de Segurança antes de começar
#     if not config.client:
#         print("ERRO: Cliente Binance não carregado no Backtest.")
#         return {"error": "Chaves da Binance não configuradas no Backend."}

#     # 1. Coleta de Dados (Limitada para performance)
#     safe_days = min(days, 365) 
    
#     try:
#         df_15m = get_historical_data(symbol, TIMEFRAME, days_back=safe_days)
#         df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=safe_days)
#         df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=safe_days + 50) 
        
#         if df_15m is None or df_15m.empty:
#             return {"error": f"Sem dados de 15m para {symbol}. Verifique se o ativo existe."}
            
#     except Exception as e:
#         return {"error": f"Erro na Binance: {str(e)}"}

#     # 2. Define Regime (Apenas para exibição no gráfico, não usado na lógica)
#     regime_bullish = check_bullish_regime(df_1d)
    
#     df = add_advanced_technical_features(df_15m)
#     df = add_multitimeframe_features(df, df_1h)
    
#     # Treina modelo rápido
#     model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
#     if not model:
#         return {"error": "Dados insuficientes para gerar sinais de IA."}

#     # 3. Simulação
#     test_size = int(len(df) * 0.3) # Testa nos últimos 30%
#     df_test = df.iloc[-test_size:].copy()
    
#     if df_test.empty:
#         return {"error": "Dataset de teste vazio."}

#     balance = 10000.0
#     position = None
#     trades = []
#     equity_curve = []
    
#     # Predição em lote (Muito mais rápido)
#     try:
#         X_test = df_test[ALL_FEATURES]
#         X_test_scaled = scaler.transform(X_test)
#         probs = model.predict_proba(X_test_scaled)[:, 1]
#         df_test['probability'] = probs
#     except Exception as e:
#         return {"error": f"Erro na predição da IA: {str(e)}"}
    
#     threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    
#     for i in range(len(df_test)):
#         row = df_test.iloc[i]
#         current_price = row['close']
#         timestamp = df_test.index[i]
#         atr = row['atr']
        
#         # Log da curva
#         if i % 4 == 0: 
#             current_equity = balance + ((current_price - position['entry_price']) * position['size'] if position else 0)
#             equity_curve.append({'time': str(timestamp), 'value': round(current_equity, 2)})

#         if position is None:
#             # === LÓGICA DE ENTRADA (SEM FILTRO DE REGIME) ===
#             # Verificamos apenas: 
#             # 1. Probabilidade da IA > Threshold
#             # 2. Tendência Local (15m) Positiva
#             if row['probability'] >= threshold and is_trending_market(row):
            
#                 amount = balance 
#                 size = amount / current_price
#                 sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
#                 tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                
#                 position = {
#                     'entry_price': current_price, 'size': size,
#                     'sl': sl, 'tp': tp, 'highest_price': current_price,
#                     'entry_time': str(timestamp)
#                 }
#                 balance = 0 
#         else:
#             # Lógica de Saída
#             position['highest_price'] = max(position['highest_price'], current_price)
#             new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
#             position['sl'] = max(position['sl'], new_sl)
            
#             reason = None
#             if current_price >= position['tp']: reason = "TAKE_PROFIT"
#             elif current_price <= position['sl']: reason = "STOP_LOSS"
            
#             if reason:
#                 pnl = (current_price - position['entry_price']) * position['size']
#                 balance = (position['size'] * current_price)
#                 trades.append({
#                     'entry_date': position['entry_time'],
#                     'exit_date': str(timestamp),
#                     'pnl': round(pnl, 2),
#                     'reason': reason
#                 })
#                 position = None

#     total_trades = len(trades)
#     wins = len([t for t in trades if t['pnl'] > 0])
#     win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
#     final_balance = balance if position is None else (balance + (position['size'] * df_test.iloc[-1]['close']))
#     total_pnl = final_balance - 10000.0

#     return {
#         "symbol": symbol,
#         "total_trades": total_trades,
#         "win_rate": round(win_rate, 2),
#         "total_pnl": round(total_pnl, 2),
#         "final_balance": round(final_balance, 2),
#         "trades": trades,
#         "equity_curve": equity_curve,
#         "regime": "IGNORADO (TESTE)" # Indica no frontend que o filtro foi ignorado
#     }








# # Lógica do "TODOS": Agora, se o símbolo for "TODOS", ele:

# # Pega as 5 maiores moedas (BTC, ETH, BNB, etc.).

# # Roda a simulação para cada uma delas.

# # Soma todo o dinheiro: Se o BTC lucrou $500 e o ETH perdeu $100, o resultado final será $400.

# # Junta todos os trades numa lista única.
# # backend/bot/backtest_engine.py
# import pandas as pd
# import numpy as np
# from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
# from backend.bot.feature_engineering import (
#     add_advanced_technical_features, add_multitimeframe_features, 
#     check_bullish_regime, is_trending_market
# )
# from backend.bot.training_manager import train_model_pipeline
# from backend.bot.data_handler import get_historical_data, get_dynamic_symbols
# from backend.config import TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO
# import backend.config as config
# from sklearn.preprocessing import StandardScaler

# def run_single_symbol_simulation(symbol, days):
#     """Executa a simulação para UM único símbolo (Lógica isolada)"""
#     safe_days = min(days, 365)
    
#     try:
#         df_15m = get_historical_data(symbol, TIMEFRAME, days_back=safe_days)
#         df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=safe_days)
#         df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=safe_days + 50) 
        
#         if df_15m is None or df_15m.empty: return None
#     except: return None

#     # Regime apenas para info (não trava a operação no teste)
#     regime_bullish = check_bullish_regime(df_1d)
    
#     df = add_advanced_technical_features(df_15m)
#     df = add_multitimeframe_features(df, df_1h)
    
#     model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
#     if not model: return None

#     test_size = int(len(df) * 0.3)
#     df_test = df.iloc[-test_size:].copy()
#     if df_test.empty: return None

#     balance = 10000.0 # Cada robô começa com 10k fictícios
#     position = None
#     trades = []
    
#     try:
#         X_test = df_test[ALL_FEATURES]
#         X_test_scaled = scaler.transform(X_test)
#         probs = model.predict_proba(X_test_scaled)[:, 1]
#         df_test['probability'] = probs
#     except: return None
    
#     threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    
#     for i in range(len(df_test)):
#         row = df_test.iloc[i]
#         current_price = row['close']
#         timestamp = df_test.index[i]
#         atr = row['atr']
        
#         if position is None:
#             # Lógica SEM filtro macro para teste de estresse
#             if row['probability'] >= threshold and is_trending_market(row):
#                 amount = balance 
#                 size = amount / current_price
#                 sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
#                 tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                
#                 position = {
#                     'entry_price': current_price, 'size': size,
#                     'sl': sl, 'tp': tp, 'highest_price': current_price,
#                     'entry_time': str(timestamp)
#                 }
#                 balance = 0 
#         else:
#             position['highest_price'] = max(position['highest_price'], current_price)
#             new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
#             position['sl'] = max(position['sl'], new_sl)
            
#             reason = None
#             if current_price >= position['tp']: reason = "TAKE_PROFIT"
#             elif current_price <= position['sl']: reason = "STOP_LOSS"
            
#             if reason:
#                 pnl = (current_price - position['entry_price']) * position['size']
#                 balance = (position['size'] * current_price)
#                 trades.append({
#                     'entry_date': position['entry_time'],
#                     'exit_date': str(timestamp),
#                     'pnl': round(pnl, 2),
#                     'reason': reason,
#                     'symbol': symbol # Identifica de qual moeda veio o trade
#                 })
#                 position = None

#     final_balance = balance if position is None else (balance + (position['size'] * df_test.iloc[-1]['close']))
#     total_pnl = final_balance - 10000.0
    
#     return {
#         'pnl': total_pnl,
#         'trades': trades,
#         'regime': regime_bullish,
#         'final_balance': final_balance
#     }

# def run_dashboard_backtest(symbol, days=60):
#     print(f"Iniciando Backtest de Dashboard para {symbol} ({days} dias)...")
    
#     if not config.client:
#         return {"error": "Chaves da Binance não configuradas no Backend."}

#     # === MODO PORTFÓLIO (TODOS) ===
#     if symbol == "TODOS":
#         # Pega Top 5 ativos para não demorar demais
#         symbols_list = get_dynamic_symbols()[:5] 
#         print(f"Modo Portfólio ativado. Simulando: {symbols_list}")
        
#         aggregated_pnl = 0
#         all_trades = []
#         wins = 0
#         total_balance = 0
        
#         for sym in symbols_list:
#             result = run_single_symbol_simulation(sym, days)
#             if result:
#                 aggregated_pnl += result['pnl']
#                 all_trades.extend(result['trades'])
#                 total_balance += result['final_balance']
        
#         # Consolida resultados
#         total_trades_count = len(all_trades)
#         wins = sum(1 for t in all_trades if t['pnl'] > 0)
#         win_rate = (wins / total_trades_count * 100) if total_trades_count > 0 else 0
        
#         # Ordena trades por data para o gráfico ficar bonito (opcional, aqui simplificado)
#         all_trades.sort(key=lambda x: x['entry_date'])
        
#         return {
#             "symbol": "PORTFOLIO (TOP 5)",
#             "total_trades": total_trades_count,
#             "win_rate": round(win_rate, 2),
#             "total_pnl": round(aggregated_pnl, 2),
#             "final_balance": round(total_balance, 2),
#             "trades": all_trades, # Lista com todos os trades de todas as moedas
#             "equity_curve": [], # Curva simplificada para não pesar
#             "regime": "MISTO"
#         }

#     # === MODO ÚNICO (Lógica antiga) ===
#     else:
#         result = run_single_symbol_simulation(symbol, days)
#         if not result:
#             return {"error": f"Falha ao simular {symbol} ou sem dados."}
            
#         total_trades = len(result['trades'])
#         wins = sum(1 for t in result['trades'] if t['pnl'] > 0)
#         win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
#         return {
#             "symbol": symbol,
#             "total_trades": total_trades,
#             "win_rate": round(win_rate, 2),
#             "total_pnl": round(result['pnl'], 2),
#             "final_balance": round(result['final_balance'], 2),
#             "trades": result['trades'],
#             "equity_curve": [],
#             "regime": "BULLISH" if result['regime'] else "BEARISH"
#         }








# # Lógica do "TODOS": Agora, se o símbolo for "TODOS", ele:

# # Pega as 5 maiores moedas (BTC, ETH, BNB, etc.).

# # Roda a simulação para cada uma delas.

# # Soma todo o dinheiro: Se o BTC lucrou $500 e o ETH perdeu $100, o resultado final será $400.

# # Junta todos os trades numa lista única.

# Gráfico Individual: Volta a calcular e enviar a linha do gráfico para simulações de uma moeda.

# Gráfico de Portfólio (TODOS): Agora ele soma o saldo de todos os robôs a cada hora para criar uma "Curva de Patrimônio Global" (ex: se você tem 5 robôs com $10k cada, o gráfico começa em $50k e oscila conforme o lucro conjunto).

# backend/bot/backtest_engine.py
import pandas as pd
import numpy as np
from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
from backend.bot.feature_engineering import (
    add_advanced_technical_features, add_multitimeframe_features, 
    check_bullish_regime, is_trending_market
)
from backend.bot.training_manager import train_model_pipeline
from backend.bot.data_handler import get_historical_data, get_dynamic_symbols
from backend.config import TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO
import backend.config as config
from sklearn.preprocessing import StandardScaler

def run_single_symbol_simulation(symbol, days):
    """Executa a simulação para UM único símbolo e retorna histórico detalhado"""
    safe_days = min(days, 365)
    
    try:
        df_15m = get_historical_data(symbol, TIMEFRAME, days_back=safe_days)
        df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=safe_days)
        df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=safe_days + 50) 
        
        if df_15m is None or df_15m.empty: return None
    except: return None

    regime_bullish = check_bullish_regime(df_1d)
    
    df = add_advanced_technical_features(df_15m)
    df = add_multitimeframe_features(df, df_1h)
    
    model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
    if not model: return None

    test_size = int(len(df) * 0.3)
    df_test = df.iloc[-test_size:].copy()
    if df_test.empty: return None

    balance = 10000.0
    position = None
    trades = []
    equity_curve = [] # Lista para armazenar o histórico do saldo
    
    try:
        X_test = df_test[ALL_FEATURES]
        X_test_scaled = scaler.transform(X_test)
        probs = model.predict_proba(X_test_scaled)[:, 1]
        df_test['probability'] = probs
    except: return None
    
    threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    
    for i in range(len(df_test)):
        row = df_test.iloc[i]
        current_price = row['close']
        timestamp = df_test.index[i]
        atr = row['atr']
        
        # --- CÁLCULO DA CURVA DE PATRIMÔNIO ---
        # Calcula o saldo flutuante (Balance + Lucro não realizado)
        current_equity = balance
        if position:
            unrealized_pnl = (current_price - position['entry_price']) * position['size']
            current_equity += unrealized_pnl
        
        # Salva o ponto no gráfico (a cada 1 hora para não pesar)
        if i % 4 == 0:
            equity_curve.append({'time': str(timestamp), 'value': round(current_equity, 2)})

        # --- LÓGICA DE TRADING ---
        if position is None:
            # SEM FILTRO MACRO PARA TESTE (Como você pediu)
            if row['probability'] >= threshold and is_trending_market(row):
                amount = balance 
                size = amount / current_price
                sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
                tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                
                position = {
                    'entry_price': current_price, 'size': size,
                    'sl': sl, 'tp': tp, 'highest_price': current_price,
                    'entry_time': str(timestamp)
                }
                balance = 0 
        else:
            position['highest_price'] = max(position['highest_price'], current_price)
            new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
            position['sl'] = max(position['sl'], new_sl)
            
            reason = None
            if current_price >= position['tp']: reason = "TAKE_PROFIT"
            elif current_price <= position['sl']: reason = "STOP_LOSS"
            
            if reason:
                pnl = (current_price - position['entry_price']) * position['size']
                balance = (position['size'] * current_price)
                trades.append({
                    'entry_date': position['entry_time'],
                    'exit_date': str(timestamp),
                    'pnl': round(pnl, 2),
                    'reason': reason,
                    'symbol': symbol
                })
                position = None

    final_balance = balance if position is None else (balance + (position['size'] * df_test.iloc[-1]['close']))
    total_pnl = final_balance - 10000.0
    
    return {
        'pnl': total_pnl,
        'trades': trades,
        'regime': regime_bullish,
        'final_balance': final_balance,
        'equity_curve': equity_curve # Retorna a curva corrigida
    }

def run_dashboard_backtest(symbol, days=60):
    print(f"Iniciando Backtest de Dashboard para {symbol} ({days} dias)...")
    
    if not config.client:
        return {"error": "Chaves da Binance não configuradas no Backend."}

    # === MODO PORTFÓLIO (TODOS) ===
    if symbol == "TODOS":
        # Pega Top 5 ativos para teste rápido (pode aumentar se quiser)
        symbols_list = get_dynamic_symbols()[:5] 
        print(f"Modo Portfólio ativado. Simulando: {symbols_list}")
        
        aggregated_pnl = 0
        all_trades = []
        total_balance = 0
        all_curves = []
        
        for sym in symbols_list:
            result = run_single_symbol_simulation(sym, days)
            if result:
                aggregated_pnl += result['pnl']
                all_trades.extend(result['trades'])
                total_balance += result['final_balance']
                # Adiciona a curva individual na lista para somar depois
                all_curves.append(result['equity_curve'])
        
        # --- COMBINAÇÃO DAS CURVAS DE PATRIMÔNIO ---
        # Cria um DataFrame para somar os valores alinhados pelo tempo
        final_equity_curve = []
        if all_curves:
            try:
                # Converte lista de dicts em DataFrames
                dfs = [pd.DataFrame(c).set_index('time') for c in all_curves]
                # Concatena alinhando pelo índice (tempo) e soma os valores
                # fillna(10000) assume que se não tem dados, o robô tinha o saldo inicial
                combined_df = pd.concat(dfs, axis=1).fillna(10000).sum(axis=1)
                
                # Converte de volta para o formato que o frontend aceita
                final_equity_curve = [{'time': t, 'value': round(v, 2)} for t, v in combined_df.items()]
                # Ordena por tempo
                final_equity_curve.sort(key=lambda x: x['time'])
            except Exception as e:
                print(f"Erro ao combinar gráficos: {e}")
                final_equity_curve = []

        total_trades_count = len(all_trades)
        wins = sum(1 for t in all_trades if t['pnl'] > 0)
        win_rate = (wins / total_trades_count * 100) if total_trades_count > 0 else 0
        all_trades.sort(key=lambda x: x['entry_date'])
        
        return {
            "symbol": "PORTFOLIO (TOP 5)",
            "total_trades": total_trades_count,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(aggregated_pnl, 2),
            "final_balance": round(total_balance, 2),
            "trades": all_trades,
            "equity_curve": final_equity_curve, # Gráfico combinado
            "regime": "MISTO"
        }

    # === MODO ÚNICO ===
    else:
        result = run_single_symbol_simulation(symbol, days)
        if not result:
            return {"error": f"Falha ao simular {symbol} ou sem dados."}
            
        total_trades = len(result['trades'])
        wins = sum(1 for t in result['trades'] if t['pnl'] > 0)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        return {
            "symbol": symbol,
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(result['pnl'], 2),
            "final_balance": round(result['final_balance'], 2),
            "trades": result['trades'],
            "equity_curve": result['equity_curve'], # Gráfico individual
            "regime": "BULLISH" if result['regime'] else "BEARISH"
        }