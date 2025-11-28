# backend/bot/feature_engineering.py
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, ADXIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from backend.config import STRATEGY_CONFIG, ADX_THRESHOLD

def add_advanced_technical_features(df, config=STRATEGY_CONFIG):
    """Calcula todas as features técnicas (RSI, EMAs, BB, etc)."""
    # print("Calculando features técnicas avançadas...")
    cfg = config['indicators']
    df['RSI'] = RSIIndicator(df['close'], window=cfg['rsi']['window']).rsi()
    df['MA_5'] = df['close'].rolling(window=cfg['ma_fast']['window']).mean()
    df['MA_10'] = df['close'].rolling(window=cfg['ma_slow']['window']).mean()
    df['EMA_50'] = EMAIndicator(df['close'], window=cfg['ema_medium']['window']).ema_indicator()
    df['EMA_200'] = EMAIndicator(df['close'], window=cfg['ema_long']['window']).ema_indicator()
    df['adx'] = ADXIndicator(df['high'], df['low'], df['close'], window=cfg['adx']['window']).adx()
    df['atr'] = AverageTrueRange(df['high'], df['low'], df['close'], window=cfg['atr']['window']).average_true_range()
    
    bb = BollingerBands(df['close'], window=cfg['bollinger']['window'], window_dev=cfg['bollinger']['window_dev'])
    df['bb_bbm'] = bb.bollinger_mavg()
    df['bb_bbh'] = bb.bollinger_hband()
    df['bb_bbl'] = bb.bollinger_lband()
    
    df['dist_ema_200_pct'] = (df['close'] - df['EMA_200']) / df['EMA_200']
    df['bb_width_pct'] = (df['bb_bbh'] - df['bb_bbl']) / df['bb_bbm']
    df['atr_pct'] = df['atr'] / df['close']
    df['day_of_week'] = df.index.dayofweek
    df['hour_of_day'] = df.index.hour
    df['ema_50_roc'] = df['EMA_50'].pct_change(periods=cfg['roc']['periods'])
    df['atr_pct_std_20'] = df['atr_pct'].rolling(window=cfg['vol_of_vol']['window']).std()
    df['rsi_x_trend'] = df['RSI'] * df['dist_ema_200_pct']
    df['rsi_lag'] = df['RSI'].shift(cfg['lags']['rsi'])
    
    return df

def add_multitimeframe_features(df_15m, df_1h):
    """Adiciona a EMA de 1h nos dados de 15m."""
    # print("Adicionando features de múltiplos timeframes...")
    df_1h['EMA_1h'] = EMAIndicator(df_1h['close'], window=21).ema_indicator()
    df_1h_feature = df_1h[['EMA_1h']].copy()
    df_1h_feature.index.name = 'timestamp'
    # Merge asof para alinhar os tempos corretamente
    df_merged = pd.merge_asof(df_15m.sort_index(), df_1h_feature.sort_index(), on='timestamp', direction='backward')
    df_merged.set_index('timestamp', inplace=True)
    return df_merged

def create_labels_with_dynamic_risk(df, config=STRATEGY_CONFIG):
    """(USADO APENAS NO TREINO) Cria os alvos (Compra=1, Nada=0)."""
    # print("Criando alvos com base em risco/retorno dinâmico (ATR)...")
    cfg = config['labeling']
    horizon_candles = int(cfg['horizon_hours'] * (60 / 15)) 
    labels = []
    
    for i in range(len(df) - horizon_candles):
        entry_price = df['close'].iloc[i]
        atr_at_entry = df['atr'].iloc[i]
        
        if atr_at_entry is None or atr_at_entry == 0 or np.isnan(atr_at_entry):
            labels.append(np.nan)
            continue
            
        take_profit_price = entry_price + (cfg['tp_atr_multiplier'] * atr_at_entry)
        stop_loss_price = entry_price - (cfg['sl_atr_multiplier'] * atr_at_entry)
        outcome = 0
        future_window = df.iloc[i+1 : i+1+horizon_candles]
        
        # Verifica se tocou no TP ou SL primeiro
        for j in range(len(future_window)):
            future_high = future_window['high'].iloc[j]
            future_low = future_window['low'].iloc[j]
            if future_high >= take_profit_price: outcome = 1; break
            if future_low <= stop_loss_price: outcome = 0; break
        labels.append(outcome)
        
    missing_labels = len(df) - len(labels)
    labels.extend([np.nan] * missing_labels)
    df['Target'] = labels
    return df

def is_trending_market(row, adx_threshold=ADX_THRESHOLD):
    """Fase 3: Lógica do Filtro Local (15m). Retorna True se tiver tendência."""
    try:
        adx_strong_enough = row['adx'] > adx_threshold
        is_uptrend_context = row['EMA_50'] > row['EMA_200']
        return adx_strong_enough and is_uptrend_context
    except KeyError:
        return False

def check_bullish_regime(df_1d, config=STRATEGY_CONFIG):
    """Fase 0: Define o Regime Macro (1d). Retorna True se Bullish."""
    try:
        window = config['regime_filter']['window']
        ema_regime = EMAIndicator(df_1d['close'], window=window).ema_indicator()
        last_close_daily = df_1d['close'].iloc[-1]
        last_ema_daily = ema_regime.iloc[-1]
        
        is_bullish = last_close_daily > last_ema_daily
        print(f"Regime Macro: {'BULLISH' if is_bullish else 'BEARISH'} (Preço: {last_close_daily:.2f} > EMA{window}: {last_ema_daily:.2f})")
        return is_bullish
    except Exception as e:
        print(f"Erro ao checar regime bullish: {e}")
        return False