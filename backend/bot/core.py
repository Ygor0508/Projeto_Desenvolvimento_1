# import time
# from datetime import datetime
# import numpy as np
# import pandas as pd
# from binance.client import Client
# from sqlalchemy.exc import IntegrityError
# from backend.models import db, Trade, OpenPosition, BotSettings, User
# from backend.utils.security import decrypt_data
# from .data_handler import get_historical_data, add_technical_indicators, add_multitimeframe_features
# from .training_manager import TrainingManager

# class TradingBot:
#     def __init__(self, user_id):
#         self.user = User.query.get(user_id)
#         if not self.user:
#             raise ValueError("Usuário não encontrado.")

#         self.api_key = decrypt_data(self.user.binance_api_key_encrypted)
#         self.api_secret = decrypt_data(self.user.binance_api_secret_encrypted)
#         self.client = Client(self.api_key, self.api_secret)
#         self.settings = BotSettings.query.filter_by(user_id=self.user.id).first()
#         self._is_running = True
#         self.training_manager = TrainingManager(self.client)
#         self.models = {}

#     def stop(self):
#         self._is_running = False

#     def run(self):
#         print(f"Iniciando o bot de trading para o usuário {self.user.username}...")
#         self.models = self.training_manager.train_all_models()
#         self.update_symbol_whitelist()

#         while self._is_running:
#             print(f"Bot em execução para {self.user.username}...")
#             self.check_for_sell_opportunities()
#             self.check_for_buy_opportunities()
#             time.sleep(60)

#         print(f"Bot parado para o usuário {self.user.username}.")

#     def update_symbol_whitelist(self):
#         profitable_symbols = [symbol for symbol, result in self.training_manager.backtest_results.items() if result.get('pnl_percent', 0) > 0 and result.get('risk_reward_ratio', 0) > 1.5]
        
#         if not self.settings:
#             self.settings = BotSettings(user_id=self.user.id)
#             db.session.add(self.settings)

#         self.settings.whitelisted_symbols = profitable_symbols
#         db.session.commit()
#         print(f"Whitelist de símbolos atualizada com {len(profitable_symbols)} pares lucrativos.")

#     def check_for_sell_opportunities(self):
#         open_positions = OpenPosition.query.filter_by(user_id=self.user.id).all()
#         for position in open_positions:
#             try:
#                 current_price = float(self.client.get_symbol_ticker(symbol=position.symbol)['price'])
#                 df = get_historical_data(self.client, position.symbol, '15m', 30)
#                 df = add_technical_indicators(df)
#                 atr_value = df['atr'].iloc[-1]

#                 take_profit_price = float(position.entry_price) + (3.0 * atr_value)
#                 stop_loss_price = float(position.entry_price) - (1.5 * atr_value)

#                 if current_price >= take_profit_price or current_price <= stop_loss_price:
#                     self.place_order(position.symbol, 'SELL', position)

#             except Exception as e:
#                 print(f"Erro ao verificar venda para {position.symbol}: {e}")

#     def check_for_buy_opportunities(self):
#         if not self.settings or not self.settings.whitelisted_symbols:
#             print("Nenhuma whitelist de símbolos definida. Pulando compras.")
#             return

#         open_positions_count = OpenPosition.query.filter_by(user_id=self.user.id).count()
#         if open_positions_count >= self.settings.max_open_positions:
#             return

#         for symbol in self.settings.whitelisted_symbols:
#             if not OpenPosition.query.filter_by(user_id=self.user.id, symbol=symbol).first():
#                 signal = self.get_trade_signal(symbol)
#                 if signal == 'BUY':
#                     self.place_order(symbol, 'BUY')

#     def get_trade_signal(self, symbol):
#         model_data = self.models.get(symbol)
#         if not model_data:
#             return 'HOLD'

#         rf_model, xgb_model, scaler, features = model_data
#         df_15m = get_historical_data(self.client, symbol, '15m', 30)
#         df_1h = get_historical_data(self.client, symbol, '1h', 60)
#         df = add_technical_indicators(df_15m)
#         df = add_multitimeframe_features(df, df_1h)

#         latest_data = df[features].iloc[-1:].values
#         latest_data_scaled = scaler.transform(latest_data)

#         rf_pred = rf_model.predict(latest_data_scaled)[0]
#         xgb_pred = xgb_model.predict(latest_data_scaled)[0]
#         prediction = int(rf_pred + xgb_pred >= 1)

#         if prediction == 1 and df['close'].iloc[-1] < df['bb_bbm'].iloc[-1] and df['adx'].iloc[-1] > 20:
#             return 'BUY'
#         return 'HOLD'

#     def place_order(self, symbol, side, position=None):
#         try:
#             if side == 'BUY':
#                 price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
#                 quantity = self.settings.trade_amount_usdt / price
#                 # Adicionar lógica de ajuste de quantidade (adjust_quantity)
#                 order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
                
#                 new_position = OpenPosition(
#                     user_id=self.user.id,
#                     symbol=symbol,
#                     entry_price=price,
#                     quantity=quantity,
#                     entry_timestamp=datetime.utcnow()
#                 )
#                 db.session.add(new_position)
#                 db.session.commit()

#             elif side == 'SELL' and position:
#                 # Adicionar lógica de ajuste de quantidade (adjust_quantity)
#                 order = self.client.order_market_sell(symbol=symbol, quantity=position.quantity)
                
#                 pnl = (float(order['fills'][0]['price']) - float(position.entry_price)) * float(position.quantity)
#                 new_trade = Trade(
#                     user_id=self.user.id,
#                     symbol=symbol,
#                     order_id=order['orderId'],
#                     side='SELL',
#                     quantity=position.quantity,
#                     price=order['fills'][0]['price'],
#                     total_value_usdt=float(order['cummulativeQuoteQty']),
#                     pnl_usdt=pnl,
#                     timestamp=datetime.utcnow()
#                 )
#                 db.session.add(new_trade)
#                 db.session.delete(position)
#                 db.session.commit()

#         except IntegrityError:
#             db.session.rollback()
#             print(f"Erro de integridade ao processar ordem para {symbol}. Posição pode já existir.")
#         except Exception as e:
#             print(f"Erro ao colocar ordem para {symbol}: {e}")

# backend/bot/core.py
import pandas as pd
import numpy as np
from backend.config import STRATEGY_CONFIG, CUSTOM_THRESHOLDS, ALL_FEATURES
from backend.bot.data_handler import get_data_for_prediction
from backend.bot.feature_engineering import (
    add_advanced_technical_features, add_multitimeframe_features, 
    is_trending_market
)
from backend.bot import bot_manager

def place_order_simulation(symbol, price, qty, type='BUY'):
    """Simula a ordem na Binance (para produção real, substituir por client.create_order)"""
    print(f"--- ORDEM {type} SIMULADA: {symbol} Qtd:{qty:.4f} Preço:{price:.2f} ---")
    return {'status': 'FILLED', 'price': price, 'executedQty': qty}

def check_symbol_logic(symbol, model, scaler, is_bullish_regime):
    """Executa a lógica (Fases 1, 3, 4)"""
    print(f"\nAnalisando {symbol}...")
    
    # Busca dados em tempo real
    df_15m, df_1h, _ = get_data_for_prediction(symbol)
    if df_15m is None: return

    # Gera features
    df = add_advanced_technical_features(df_15m)
    df = add_multitimeframe_features(df, df_1h)
    
    # Pega o último candle fechado (penúltimo do array)
    if len(df) < 2: return
    last_row = df.iloc[-2]
    
    # --- Fase 1: Previsão da IA ---
    # Prepara dados para o modelo
    X_latest = pd.DataFrame([last_row[ALL_FEATURES]])
    X_scaled = scaler.transform(X_latest)
    probability = model.predict_proba(X_scaled)[0, 1]
    
    threshold = CUSTOM_THRESHOLDS.get(symbol, 0.5) # Threshold customizado
    prediction = 1 if probability >= threshold else 0
    
    print(f"[{symbol}] IA Prob: {probability:.2f} (Gatilho: {threshold}) -> Sinal: {prediction}")

    # --- Gestão ---
    current_price = last_row['close']
    atr = last_row['atr']
    position = bot_manager.get_position(symbol)

    if position is None:
        # --- Fase 3: Lógica de Entrada ---
        # 1. Sem posição
        # 2. Sinal da IA (prediction == 1)
        if prediction == 1:
            # 3. Filtro Macro (Regime Bullish)
            if is_bullish_regime:
                # 4. Filtro Local (Tendência)
                if is_trending_market(last_row):
                    print(f"+++ COMPRA DETECTADA: {symbol} +++")
                    # Compra simulada de $1000 USDT
                    qty = 1000 / current_price
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
                    print("Sinal ignorado: Filtro Local (ADX/EMA) falhou.")
            else:
                print("Sinal ignorado: Filtro Macro (Regime Bearish).")
    
    else:
        # --- Fase 4: Lógica de Saída ---
        print(f"Gerenciando Posição {symbol}...")
        
        # Atualiza Trailing Stop
        position['highest_price'] = max(position['highest_price'], current_price)
        new_sl = position['highest_price'] - (STRATEGY_CONFIG['trailing_sl']['atr_multiplier'] * atr)
        position['trailing_stop'] = max(position['trailing_stop'], new_sl)
        
        # Calcula TP
        tp_price = position['entry_price'] + (STRATEGY_CONFIG['labeling']['tp_atr_multiplier'] * atr)
        
        print(f"Preço: {current_price:.2f} | SL: {position['trailing_stop']:.2f} | TP: {tp_price:.2f}")

        if current_price >= tp_price:
            print(f"--- VENDA (TAKE PROFIT): {symbol} ---")
            place_order_simulation(symbol, current_price, position['position_size'], 'SELL')
            bot_manager.update_position(symbol, None)
            
        elif current_price <= position['trailing_stop']:
            print(f"--- VENDA (STOP LOSS): {symbol} ---")
            place_order_simulation(symbol, current_price, position['position_size'], 'SELL')
            bot_manager.update_position(symbol, None)