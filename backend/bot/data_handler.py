# import time
# import pandas as pd
# import numpy as np
# from binance.client import Client
# from ta.momentum import RSIIndicator
# from ta.trend import EMAIndicator, ADXIndicator
# from ta.volatility import BollingerBands, AverageTrueRange

# def get_historical_data(client, symbol, interval, days_back):
#     """Busca dados históricos da Binance de forma robusta."""
#     try:
#         start_ts = int((time.time() - (days_back * 24 * 60 * 60)) * 1000)
#         start_str = str(start_ts)
        
#         all_klines = []
#         while True:
#             klines = client.get_historical_klines(
#                 symbol=symbol,
#                 interval=interval,
#                 start_str=start_str,
#                 limit=1000
#             )
#             if not klines:
#                 break
#             all_klines.extend(klines)
#             start_str = str(klines[-1][0] + 1)

#         if not all_klines:
#             print(f"Nenhum dado histórico encontrado para {symbol} no timeframe {interval}.")
#             return None

#         df = pd.DataFrame(all_klines, columns=[
#             'timestamp', 'open', 'high', 'low', 'close', 'volume', 
#             'close_time', 'quote_asset_volume', 'number_of_trades',
#             'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
#         ])
        
#         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#         df.set_index('timestamp', inplace=True)
        
#         for col in ['open', 'high', 'low', 'close', 'volume']:
#             df[col] = df[col].astype(float)
            
#         return df[['open', 'high', 'low', 'close', 'volume']]
#     except Exception as e:
#         print(f"Erro ao obter dados históricos para {symbol} ({interval}): {e}")
#         return None

# def add_technical_indicators(df):
#     """Adiciona um conjunto rico de indicadores técnicos ao DataFrame."""
#     df['RSI'] = RSIIndicator(df['close'], window=14).rsi()
#     df['EMA'] = EMAIndicator(df['close'], window=14).ema_indicator()
#     bb_indicator = BollingerBands(df['close'], window=20, window_dev=2)
#     df['bb_bbm'] = bb_indicator.bollinger_mavg()
#     df['bb_bbh'] = bb_indicator.bollinger_hband()
#     df['bb_bbl'] = bb_indicator.bollinger_lband()
#     df['MA_5'] = df['close'].rolling(window=5).mean()
#     df['MA_10'] = df['close'].rolling(window=10).mean()
#     df['StdDev'] = df['close'].rolling(window=5).std()
#     df['Momentum'] = df['close'].diff(4)
#     df['MACD'] = EMAIndicator(df['close'], window=12).ema_indicator() - EMAIndicator(df['close'], window=26).ema_indicator()
#     adx_indicator = ADXIndicator(df['high'], df['low'], df['close'], window=14)
#     df['adx'] = adx_indicator.adx()
#     df['atr'] = AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
    
#     df.replace([np.inf, -np.inf], np.nan, inplace=True)
#     df.ffill(inplace=True)
#     df.bfill(inplace=True)
    
#     return df

# def add_multitimeframe_features(df_15m, df_1h):
#     """Adiciona features do timeframe maior (1h) ao dataframe principal (15m)."""
#     df_1h['EMA_1h'] = EMAIndicator(df_1h['close'], window=21).ema_indicator()
#     df_1h_feature = df_1h[['EMA_1h']].copy()
#     df_1h_feature.index.name = 'timestamp'
#     df_merged = pd.merge_asof(df_15m.sort_index(), df_1h_feature.sort_index(), on='timestamp', direction='backward')
#     df_merged.set_index('timestamp', inplace=True)
#     return df_merged






# # backend/bot/data_handler.py
# import pandas as pd
# import numpy as np
# import time
# from backend.config import client, MIN_VOLUME_USDT, SYMBOL_BLACKLIST, TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO

# def get_dynamic_symbols(quote_asset='USDT', min_24h_volume_usdt=MIN_VOLUME_USDT):
#     """Fase 0: Filtro de Volume e Blacklist"""
#     print(f"Buscando símbolos com volume > ${min_24h_volume_usdt:,} USDT...")
#     try:
#         all_tickers = client.get_ticker()
#         exchange_info = client.get_exchange_info()
#         trading_symbols_info = {s['symbol']: s for s in exchange_info['symbols'] if s['status'] == 'TRADING'}
        
#         symbols = [
#             ticker['symbol'] for ticker in all_tickers
#             if ticker['symbol'].endswith(quote_asset) and
#             float(ticker['quoteVolume']) > min_24h_volume_usdt and
#             ticker['symbol'] in trading_symbols_info and
#             ticker['symbol'] not in SYMBOL_BLACKLIST
#         ]
#         print(f"Encontrados {len(symbols)} símbolos ativos.")
#         return symbols
#     except Exception as e:
#         print(f"Erro ao buscar símbolos: {e}")
#         return ["BTCUSDT", "ETHUSDT", "BNBUSDT"] 

# def get_historical_data(symbol, interval, days_back):
#     """Pega os dados históricos (Candles)"""
#     try:
#         start_ts = int((time.time() - (days_back * 24 * 60 * 60)) * 1000)
#         start_str = str(start_ts)
#         all_klines = []
        
#         # Paginação para pegar mais de 1000 candles
#         while True:
#             klines = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_str, limit=1000)
#             if not klines: break
#             all_klines.extend(klines)
#             start_str = str(klines[-1][0] + 1)
#             # break # Remova este break se quiser muitos dados, deixei por segurança pra não estourar cota no teste

#         if not all_klines: return None

#         df = pd.DataFrame(all_klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
#         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#         df.set_index('timestamp', inplace=True)
#         for col in ['open', 'high', 'low', 'close', 'volume']:
#             df[col] = df[col].astype(float)
        
#         return df[['open', 'high', 'low', 'close', 'volume']]
#     except Exception as e:
#         print(f"Erro ao obter dados para {symbol} ({interval}): {e}")
#         return None

# def get_data_for_prediction(symbol):
#     """Pega dados recentes (15m, 1h, 1d) para rodar o robô em tempo real."""
#     try:
#         # Pega dados suficientes para calcular indicadores (ex: EMA 200 precisa de 200 candles)
#         df_15m = get_historical_data(symbol, TIMEFRAME, days_back=5)
#         df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=20)
#         df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=200) # Precisa de bastante para EMA50 diária
        
#         if any(df is None or df.empty for df in [df_15m, df_1h, df_1d]):
#             return None, None, None
            
#         return df_15m, df_1h, df_1d
#     except Exception as e:
#         print(f"Erro em get_data_for_prediction: {e}")
#         return None, None, None




# backend/bot/data_handler.py
import pandas as pd
import numpy as np
import time
# ALTERADO: Importamos o módulo 'config' inteiro para acessar o client atualizado dinamicamente
import backend.config as config 
from backend.config import MIN_VOLUME_USDT, SYMBOL_BLACKLIST, TIMEFRAME, TIMEFRAME_MAIOR, TIMEFRAME_MACRO

def get_dynamic_symbols(quote_asset='USDT', min_24h_volume_usdt=MIN_VOLUME_USDT):
    """Fase 0: Filtro de Volume e Blacklist"""
    # Verificação de segurança
    if not config.client:
        print("AVISO: Cliente Binance não inicializado. Configure as chaves no Dashboard.")
        return []

    print(f"Buscando símbolos com volume > ${min_24h_volume_usdt:,} USDT...")
    try:
        # Usa config.client em vez de client direto
        all_tickers = config.client.get_ticker() 
        exchange_info = config.client.get_exchange_info()
        trading_symbols_info = {s['symbol']: s for s in exchange_info['symbols'] if s['status'] == 'TRADING'}
        
        symbols = [
            ticker['symbol'] for ticker in all_tickers
            if ticker['symbol'].endswith(quote_asset) and
            float(ticker['quoteVolume']) > min_24h_volume_usdt and
            ticker['symbol'] in trading_symbols_info and
            ticker['symbol'] not in SYMBOL_BLACKLIST
        ]
        print(f"Encontrados {len(symbols)} símbolos ativos.")
        return symbols
    except Exception as e:
        print(f"Erro ao buscar símbolos: {e}")
        # Retorna lista vazia ou fallback seguro para não quebrar o loop
        return ["BTCUSDT", "ETHUSDT", "BNBUSDT"] 

def get_historical_data(symbol, interval, days_back):
    """Pega os dados históricos (Candles)"""
    if not config.client:
        print("AVISO: Cliente Binance não inicializado.")
        return None

    try:
        start_ts = int((time.time() - (days_back * 24 * 60 * 60)) * 1000)
        start_str = str(start_ts)
        all_klines = []
        
        while True:
            klines = config.client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_str, limit=1000)
            if not klines: break
            all_klines.extend(klines)
            start_str = str(klines[-1][0] + 1)

        if not all_klines: return None

        df = pd.DataFrame(all_klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        return df[['open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        print(f"Erro ao obter dados para {symbol} ({interval}): {e}")
        return None

def get_data_for_prediction(symbol):
    """Pega dados recentes (15m, 1h, 1d) para rodar o robô em tempo real."""
    if not config.client:
        return None, None, None

    try:
        df_15m = get_historical_data(symbol, TIMEFRAME, days_back=5)
        df_1h = get_historical_data(symbol, TIMEFRAME_MAIOR, days_back=20)
        df_1d = get_historical_data(symbol, TIMEFRAME_MACRO, days_back=200) 
        
        if any(df is None or df.empty for df in [df_15m, df_1h, df_1d]):
            return None, None, None
            
        return df_15m, df_1h, df_1d
    except Exception as e:
        print(f"Erro em get_data_for_prediction: {e}")
        return None, None, None