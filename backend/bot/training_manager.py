import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from .data_handler import get_historical_data, add_technical_indicators, add_multitimeframe_features

class TrainingManager:
    def __init__(self, client):
        self.client = client
        self.backtest_results = {}

    def train_all_models(self):
        models = {}
        symbols = self.get_dynamic_symbols()
        for symbol in symbols[:20]: # Limitar a 20 símbolos para o treinamento inicial
            print(f"\n--- Treinando modelo para {symbol} ---")
            model_data = self.train_model_for_symbol(symbol)
            if model_data:
                models[symbol] = model_data
        return models

    def get_dynamic_symbols(self, quote_asset=
'USDT'
, min_24h_volume_usdt=1000000):
        try:
            all_tickers = self.client.get_ticker()
            symbols = [t['symbol'] for t in all_tickers if t['symbol'].endswith(quote_asset) and float(t['quoteVolume']) > min_24h_volume_usdt]
            return symbols
        except Exception as e:
            print(f"Erro ao buscar símbolos: {e}")
            return ["BTCUSDT", "ETHUSDT"]

    def train_model_for_symbol(self, symbol):
        try:
            df_15m = get_historical_data(self.client, symbol, '15m', 365)
            df_1h = get_historical_data(self.client, symbol, '1h', 365)
            if df_15m is None or df_1h is None or df_15m.empty or df_1h.empty:
                return None

            df = add_technical_indicators(df_15m)
            df = add_multitimeframe_features(df, df_1h)
            df = self.create_labels(df)
            df.dropna(inplace=True)

            if len(df) < 500 or df['Target'].nunique() < 2:
                return None

            features = [
                'RSI', 'EMA', 'volume', 'MA_5', 'MA_10', 'StdDev', 'Momentum', 'MACD',
                'bb_bbm', 'bb_bbh', 'bb_bbl', 'adx', 'atr', 'EMA_1h'
            ]
            
            train_size = int(len(df) * 0.8)
            df_train, df_test = df.iloc[:train_size], df.iloc[train_size:]

            X_train = df_train[features].values
            y_train = df_train['Target'].values
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            
            rf_model = RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1, n_estimators=100, max_depth=20, min_samples_leaf=5).fit(X_train_scaled, y_train)
            
            count_neg, count_pos = np.bincount(y_train)
            scale_pos_weight = count_neg / count_pos if count_pos > 0 else 1
            xgb_model = XGBClassifier(eval_metric='logloss', random_state=42, scale_pos_weight=scale_pos_weight).fit(X_train_scaled, y_train)

            self.run_backtest(symbol, df_test.copy(), rf_model, xgb_model, scaler, features)

            return rf_model, xgb_model, scaler, features

        except Exception as e:
            print(f"Erro no treinamento para {symbol}: {e}")
            return None

    def create_labels(self, df, take_profit_pct=0.015, stop_loss_pct=0.005, horizon_hours=24):
        horizon_candles = int(horizon_hours * (60 / 15))
        labels = pd.Series(np.nan, index=df.index)

        for i in range(len(df) - horizon_candles):
            entry_price = df['close'].iloc[i]
            take_profit_price = entry_price * (1 + take_profit_pct)
            stop_loss_price = entry_price * (1 - stop_loss_pct)
            
            future_window = df.iloc[i+1 : i+1+horizon_candles]
            
            tp_hit_time = future_window[future_window['high'] >= take_profit_price].index.min()
            sl_hit_time = future_window[future_window['low'] <= stop_loss_price].index.min()

            if pd.notna(tp_hit_time) and (pd.isna(sl_hit_time) or tp_hit_time < sl_hit_time):
                labels.iloc[i] = 1
            elif pd.notna(sl_hit_time):
                labels.iloc[i] = 0

        df['Target'] = labels
        return df

    def run_backtest(self, symbol, df_test, rf_model, xgb_model, scaler, features):
        X_test = df_test[features].values
        X_test_scaled = scaler.transform(X_test)

        rf_pred = rf_model.predict(X_test_scaled)
        xgb_pred = xgb_model.predict(X_test_scaled)
        final_predictions = (rf_pred + xgb_pred >= 1).astype(int)
        
        df_test['prediction'] = final_predictions
        
        initial_balance = 10000.0
        balance = initial_balance
        position = 0.0
        entry_price = 0.0
        trades = []

        for i in range(len(df_test)):
            row = df_test.iloc[i]
            if position == 0 and row['prediction'] == 1 and row['close'] < row['bb_bbm'] and row['adx'] > 20:
                position = balance / row['close']
                entry_price = row['close']
                balance = 0.0
            elif position > 0:
                take_profit = entry_price + (3.0 * row['atr'])
                stop_loss = entry_price - (1.5 * row['atr'])
                if row['close'] >= take_profit or row['close'] <= stop_loss:
                    balance = position * row['close']
                    pnl = balance - (position * entry_price)
                    trades.append({'pnl': pnl})
                    position = 0.0

        final_balance = balance if position == 0 else position * df_test['close'].iloc[-1]
        total_pnl = final_balance - initial_balance
        pnl_percent = (total_pnl / initial_balance) * 100

        wins = sum(1 for t in trades if t['pnl'] > 0)
        losses = len(trades) - wins
        win_rate = (wins / len(trades)) * 100 if trades else 0
        avg_win = np.mean([t['pnl'] for t in trades if t['pnl'] > 0]) if wins > 0 else 0
        avg_loss = abs(np.mean([t['pnl'] for t in trades if t['pnl'] < 0])) if losses > 0 else 0
        rr_ratio = avg_win / avg_loss if losses > 0 and avg_loss > 0 else 0

        self.backtest_results[symbol] = {
            'pnl_percent': pnl_percent,
            'win_rate': win_rate,
            'risk_reward_ratio': rr_ratio,
            'trades': len(trades)
        }
        print(f"Backtest para {symbol}: PnL={pnl_percent:.2f}%, WinRate={win_rate:.2f}%, RR={rr_ratio:.2f}")

