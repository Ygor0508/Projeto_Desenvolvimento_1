import pandas as pd
import numpy as np
from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
from backend.bot.data_handler import get_data_for_prediction
from backend.bot.feature_engineering import (
    add_advanced_technical_features, add_multitimeframe_features, 
    is_trending_market
)
from backend.bot import bot_manager
from backend.models import BotSettings, db 

def place_order_simulation(symbol, price, qty, type='BUY'):
    print(f"--- ORDEM {type} SIMULADA: {symbol} Qtd:{qty:.6f} Preço:{price:.2f} Total:${(qty*price):.2f} ---")
    return {'status': 'FILLED', 'price': price, 'executedQty': qty}

def check_symbol_logic(symbol, model, scaler, is_bullish_regime):
    print(f"\nAnalisando {symbol}...")
    
    # Carrega configs do banco (Regime + Valor da Ordem)
    try:
        from backend.app import app
        with app.app_context():
            settings = BotSettings.query.first()
            use_macro = settings.use_macro_regime if settings else True
            trade_amount = float(settings.trade_amount_usdt) if settings else 10.0
    except:
        use_macro = True
        trade_amount = 10.0

    df_15m, df_1h, _ = get_data_for_prediction(symbol)
    if df_15m is None: return

    df = add_advanced_technical_features(df_15m)
    df = add_multitimeframe_features(df, df_1h)
    
    if len(df) < 2: return
    last_row = df.iloc[-2]
    
    X_latest = pd.DataFrame([last_row[ALL_FEATURES]])
    X_scaled = scaler.transform(X_latest)
    probability = model.predict_proba(X_scaled)[0, 1]
    
    threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5)
    prediction = 1 if probability >= threshold else 0
    
    print(f"[{symbol}] IA Prob: {probability:.2f} (Gatilho: {threshold}) -> Sinal: {prediction}")

    current_price = last_row['close']
    atr = last_row['atr']
    position = bot_manager.get_position(symbol)

    if position is None:
        if prediction == 1:
            regime_pass = True
            if use_macro:
                if not is_bullish_regime:
                    print(f"[{symbol}] Sinal ignorado: Filtro Macro (Regime Bearish).")
                    regime_pass = False
            
            if regime_pass:
                if is_trending_market(last_row):
                    print(f"+++ COMPRA DETECTADA: {symbol} +++")
                    
                    # Cálculo da quantidade exata baseado no valor em Dólar ($)
                    qty = trade_amount / current_price
                    
                    res = place_order_simulation(symbol, current_price, qty, 'BUY')
                    
                    if res['status'] == 'FILLED':
                        entry = float(res['price'])
                        sl = entry - (STRATEGY_CONFIG['labeling']['sl_atr_multiplier'] * atr)
                        
                        bot_manager.update_position(symbol, {
                            'entry_price': entry,
                            'position_size': float(res['executedQty']),
                            'highest_price': entry,
                            'trailing_stop': sl
                        })
                else:
                    print(f"[{symbol}] Sinal ignorado: Filtro Local (ADX/EMA) falhou.")
    else:
        print(f"Gerenciando Posição {symbol}...")
        position['highest_price'] = max(position['highest_price'], current_price)
        new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
        position['trailing_stop'] = max(position['trailing_stop'], new_sl)
        
        tp_price = position['entry_price'] + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
        
        if current_price >= tp_price:
            print(f"--- VENDA (TAKE PROFIT): {symbol} ---")
            place_order_simulation(symbol, current_price, position['position_size'], 'SELL')
            bot_manager.update_position(symbol, None)
        elif current_price <= position['trailing_stop']:
            print(f"--- VENDA (STOP LOSS): {symbol} ---")
            place_order_simulation(symbol, current_price, position['position_size'], 'SELL')
            bot_manager.update_position(symbol, None)