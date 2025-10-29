import time
from datetime import datetime
import numpy as np
import pandas as pd
from binance.client import Client
from sqlalchemy.exc import IntegrityError
from backend.models import db, Trade, OpenPosition, BotSettings, User
from backend.utils.security import decrypt_data
from .data_handler import get_historical_data, add_technical_indicators, add_multitimeframe_features
from .training_manager import TrainingManager

class TradingBot:
    def __init__(self, user_id):
        self.user = User.query.get(user_id)
        if not self.user:
            raise ValueError("Usuário não encontrado.")

        self.api_key = decrypt_data(self.user.binance_api_key_encrypted)
        self.api_secret = decrypt_data(self.user.binance_api_secret_encrypted)
        self.client = Client(self.api_key, self.api_secret)
        self.settings = BotSettings.query.filter_by(user_id=self.user.id).first()
        self._is_running = True
        self.training_manager = TrainingManager(self.client)
        self.models = {}

    def stop(self):
        self._is_running = False

    def run(self):
        print(f"Iniciando o bot de trading para o usuário {self.user.username}...")
        self.models = self.training_manager.train_all_models()
        self.update_symbol_whitelist()

        while self._is_running:
            print(f"Bot em execução para {self.user.username}...")
            self.check_for_sell_opportunities()
            self.check_for_buy_opportunities()
            time.sleep(60)

        print(f"Bot parado para o usuário {self.user.username}.")

    def update_symbol_whitelist(self):
        profitable_symbols = [symbol for symbol, result in self.training_manager.backtest_results.items() if result.get('pnl_percent', 0) > 0 and result.get('risk_reward_ratio', 0) > 1.5]
        
        if not self.settings:
            self.settings = BotSettings(user_id=self.user.id)
            db.session.add(self.settings)

        self.settings.whitelisted_symbols = profitable_symbols
        db.session.commit()
        print(f"Whitelist de símbolos atualizada com {len(profitable_symbols)} pares lucrativos.")

    def check_for_sell_opportunities(self):
        open_positions = OpenPosition.query.filter_by(user_id=self.user.id).all()
        for position in open_positions:
            try:
                current_price = float(self.client.get_symbol_ticker(symbol=position.symbol)['price'])
                df = get_historical_data(self.client, position.symbol, '15m', 30)
                df = add_technical_indicators(df)
                atr_value = df['atr'].iloc[-1]

                take_profit_price = float(position.entry_price) + (3.0 * atr_value)
                stop_loss_price = float(position.entry_price) - (1.5 * atr_value)

                if current_price >= take_profit_price or current_price <= stop_loss_price:
                    self.place_order(position.symbol, 'SELL', position)

            except Exception as e:
                print(f"Erro ao verificar venda para {position.symbol}: {e}")

    def check_for_buy_opportunities(self):
        if not self.settings or not self.settings.whitelisted_symbols:
            print("Nenhuma whitelist de símbolos definida. Pulando compras.")
            return

        open_positions_count = OpenPosition.query.filter_by(user_id=self.user.id).count()
        if open_positions_count >= self.settings.max_open_positions:
            return

        for symbol in self.settings.whitelisted_symbols:
            if not OpenPosition.query.filter_by(user_id=self.user.id, symbol=symbol).first():
                signal = self.get_trade_signal(symbol)
                if signal == 'BUY':
                    self.place_order(symbol, 'BUY')

    def get_trade_signal(self, symbol):
        model_data = self.models.get(symbol)
        if not model_data:
            return 'HOLD'

        rf_model, xgb_model, scaler, features = model_data
        df_15m = get_historical_data(self.client, symbol, '15m', 30)
        df_1h = get_historical_data(self.client, symbol, '1h', 60)
        df = add_technical_indicators(df_15m)
        df = add_multitimeframe_features(df, df_1h)

        latest_data = df[features].iloc[-1:].values
        latest_data_scaled = scaler.transform(latest_data)

        rf_pred = rf_model.predict(latest_data_scaled)[0]
        xgb_pred = xgb_model.predict(latest_data_scaled)[0]
        prediction = int(rf_pred + xgb_pred >= 1)

        if prediction == 1 and df['close'].iloc[-1] < df['bb_bbm'].iloc[-1] and df['adx'].iloc[-1] > 20:
            return 'BUY'
        return 'HOLD'

    def place_order(self, symbol, side, position=None):
        try:
            if side == 'BUY':
                price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                quantity = self.settings.trade_amount_usdt / price
                # Adicionar lógica de ajuste de quantidade (adjust_quantity)
                order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
                
                new_position = OpenPosition(
                    user_id=self.user.id,
                    symbol=symbol,
                    entry_price=price,
                    quantity=quantity,
                    entry_timestamp=datetime.utcnow()
                )
                db.session.add(new_position)
                db.session.commit()

            elif side == 'SELL' and position:
                # Adicionar lógica de ajuste de quantidade (adjust_quantity)
                order = self.client.order_market_sell(symbol=symbol, quantity=position.quantity)
                
                pnl = (float(order['fills'][0]['price']) - float(position.entry_price)) * float(position.quantity)
                new_trade = Trade(
                    user_id=self.user.id,
                    symbol=symbol,
                    order_id=order['orderId'],
                    side='SELL',
                    quantity=position.quantity,
                    price=order['fills'][0]['price'],
                    total_value_usdt=float(order['cummulativeQuoteQty']),
                    pnl_usdt=pnl,
                    timestamp=datetime.utcnow()
                )
                db.session.add(new_trade)
                db.session.delete(position)
                db.session.commit()

        except IntegrityError:
            db.session.rollback()
            print(f"Erro de integridade ao processar ordem para {symbol}. Posição pode já existir.")
        except Exception as e:
            print(f"Erro ao colocar ordem para {symbol}: {e}")

