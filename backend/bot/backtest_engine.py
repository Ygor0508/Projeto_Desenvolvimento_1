import pandas as pd
import numpy as np
import concurrent.futures
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

def run_single_symbol_simulation(symbol, days, use_macro_regime, initial_capital):
    safe_days = min(days, 365)
    try:
        df_15m = get_historical_data(symbol, TIMEFRAME, days_back=safe_days)
        if df_15m is None or df_15m.empty: return None
        df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=safe_days)
        df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=safe_days + 50) 
    except: return None

    is_bullish = check_bullish_regime(df_1d)
    df = add_advanced_technical_features(df_15m)
    df = add_multitimeframe_features(df, df_1h)
    model, scaler = train_model_pipeline(df_15m, df_1h, symbol)
    if not model: return None

    test_size = int(len(df) * 0.3)
    df_test = df.iloc[-test_size:].copy()
    if df_test.empty: return None

    balance = float(initial_capital)
    position = None
    trades = []
    equity_curve = []
    
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
        
        current_equity = balance
        if position:
            unrealized = (current_price - position['entry_price']) * position['size']
            current_equity += unrealized
        
        if i % 4 == 0: 
            equity_curve.append({'time': str(timestamp), 'value': round(current_equity, 2)})

        if position is None:
            ia_signal = row['probability'] >= threshold
            macro_pass = True
            if use_macro_regime:
                if not is_bullish: macro_pass = False
            local_pass = is_trending_market(row)

            if ia_signal and macro_pass and local_pass:
                amount = balance 
                size = amount / current_price
                sl = current_price - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
                tp = current_price + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
                position = {'entry_price': current_price, 'size': size, 'sl': sl, 'tp': tp, 'highest_price': current_price, 'entry_time': str(timestamp)}
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
                trades.append({'entry_date': position['entry_time'], 'exit_date': str(timestamp), 'pnl': round(pnl, 2), 'reason': reason, 'symbol': symbol})
                position = None

    final_balance = balance if position is None else (balance + (position['size'] * df_test.iloc[-1]['close']))
    total_pnl = final_balance - float(initial_capital)
    total_trades = len(trades)
    wins = sum(1 for t in trades if t['pnl'] > 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

    return {'symbol': symbol, 'pnl': round(total_pnl, 2), 'trades': trades, 'regime': "BULLISH" if is_bullish else "BEARISH", 'final_balance': round(final_balance, 2), 'equity_curve': equity_curve, 'win_rate': round(win_rate, 1), 'total_trades': total_trades}

def run_dashboard_backtest(symbols_input, days, use_macro_regime, initial_capital):
    if isinstance(symbols_input, str): symbols_list = [symbols_input]
    else: symbols_list = symbols_input

    print(f"Iniciando Backtest Paralelo para: {len(symbols_list)} ativos. Dias: {days}.")
    if not config.client: return {"error": "Chaves da Binance não configuradas."}

    aggregated_pnl = 0
    all_trades = []
    total_balance = 0
    all_curves = []
    detailed_results = [] 

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_symbol = {executor.submit(run_single_symbol_simulation, sym, days, use_macro_regime, initial_capital): sym for sym in symbols_list}
        
        for future in concurrent.futures.as_completed(future_to_symbol):
            sym = future_to_symbol[future]
            try:
                result = future.result()
                if result:
                    print(f"-> {sym} finalizado.")
                    aggregated_pnl += result['pnl']
                    all_trades.extend(result['trades'])
                    total_balance += result['final_balance']
                    all_curves.append(result['equity_curve'])
                    detailed_results.append({'symbol': result['symbol'], 'pnl': result['pnl'], 'win_rate': result['win_rate'], 'total_trades': result['total_trades'], 'regime': result['regime'], 'equity_curve': result['equity_curve']})
            except Exception as exc: print(f"-> {sym} exceção: {exc}")

    if not detailed_results: return {"error": "Nenhum dado retornado."}

    final_equity_curve = []
    if all_curves:
        try:
            dfs = [pd.DataFrame(c).set_index('time') for c in all_curves if c]
            if dfs:
                combined_df = pd.concat(dfs, axis=1).fillna(float(initial_capital)).sum(axis=1)
                final_equity_curve = [{'time': str(t), 'value': round(v, 2)} for t, v in combined_df.items()]
                final_equity_curve.sort(key=lambda x: x['time'])
        except Exception as e: print(f"Erro curvas: {e}")

    total_trades_count = len(all_trades)
    wins = sum(1 for t in all_trades if t['pnl'] > 0)
    win_rate = (wins / total_trades_count * 100) if total_trades_count > 0 else 0
    all_trades.sort(key=lambda x: x['entry_date'])
    
    return {"symbol": "PORTFOLIO", "total_trades": total_trades_count, "win_rate": round(win_rate, 2), "total_pnl": round(aggregated_pnl, 2), "final_balance": round(total_balance, 2), "trades": all_trades, "equity_curve": final_equity_curve, "regime": "MISTO", "details": detailed_results}