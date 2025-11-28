# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#     #     'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8'
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False





# import os
# from dotenv import load_dotenv
# from binance.client import Client

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# # --- Configurações da API Binance ---
# API_KEY = os.getenv("API_KEY", "SEU_API_KEY_AQUI")
# API_SECRET = os.getenv("API_SECRET", "SEU_API_SECRET_AQUI")
# client = Client(API_KEY, API_SECRET)

# # --- Parâmetros do Bot ---
# TIMEFRAME = '15m'
# TIMEFRAME_MAIOR = '1h'
# TIMEFRAME_MACRO = '1d' 
# # MIN_VOLUME_USDT = 50000000
# MIN_VOLUME_USDT = 1000000
# ADX_THRESHOLD = 25 

# # --- Diretórios ---
# base_directory = os.path.abspath(os.path.dirname(__file__))
# trading_directory = os.path.join(base_directory, "trading_data")
# log_file_path = os.path.join(trading_directory, "trading_log_v3.1.txt")
# training_log_file_path = os.path.join(trading_directory, "training_melhoria_v3.1.txt")
# plots_directory = os.path.join(trading_directory, "feature_importance_plots")
# confusion_matrix_directory = os.path.join(trading_directory, "confusion_matrix_plots")
# models_directory = os.path.join(trading_directory, "models")

# # Cria diretórios se não existirem
# os.makedirs(trading_directory, exist_ok=True)
# os.makedirs(plots_directory, exist_ok=True)
# os.makedirs(confusion_matrix_directory, exist_ok=True)
# os.makedirs(models_directory, exist_ok=True)

# # --- Gestão de Ativos (Blacklist e Thresholds) ---
# SYMBOL_BLACKLIST = [
#     'SOLUSDT', 'ENAUSDT', 'PEPEUSDT', 'DOGEUSDT', 'SUIUSDT', '1000CHEEMSUSDT',
#     'ADAUSDT', 'TRXUSDT', 'XRPUSDT', 'LTCUSDT', 'PAXGUSDT',
#     'FDUSDUSDT', 'USDCUSDT', 'USDEUSDT'
# ]

# CUSTOM_THRESHOLDS = {
#     'BNBUSDT': 0.60,
#     # Outros ativos usam o padrão 0.50
# }

# # --- Configuração da Estratégia ---
# STRATEGY_CONFIG = {
#     'indicators': {
#         'rsi': {'window': 14}, 'bollinger': {'window': 20, 'window_dev': 2},
#         'ma_fast': {'window': 5}, 'ma_slow': {'window': 10},
#         'ema_medium': {'window': 50}, 'ema_long': {'window': 200},
#         'adx': {'window': 14}, 'atr': {'window': 14}, 'roc': {'periods': 5},
#         'vol_of_vol': {'window': 20}, 'lags': {'rsi': 3}
#     },
#     'labeling': {
#         'horizon_hours': 24, 'tp_atr_multiplier': 3.0, 'sl_atr_multiplier': 1.5
#     },
#     'regime_filter': { 
#         'window': 50
#     },
#     'trailing_sl': {
#         'atr_multiplier': 2.5
#     }
# }

# # --- Lista de Features ---
# ALL_FEATURES = [
#     'RSI', 'MA_5', 'MA_10', 'EMA_50', 'EMA_200', 'adx', 'atr', 'volume', 
#     'bb_bbm', 'bb_bbh', 'bb_bbl', 'dist_ema_200_pct', 'bb_width_pct', 
#     'atr_pct', 'EMA_1h', 'day_of_week', 'hour_of_day', 'ema_50_roc', 
#     'atr_pct_std_20', 'rsi_x_trend', 'rsi_lag'
# ]








# backend/config.py
import os
import json
from dotenv import load_dotenv
from binance.client import Client
from cryptography.fernet import Fernet

load_dotenv()

# --- Configurações do Flask ---
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://trading_bot_user:password@localhost/trading_bot_db?client_encoding=utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



# --- Diretórios ---
base_directory = os.path.abspath(os.path.dirname(__file__))
trading_directory = os.path.join(base_directory, "trading_data")
secrets_file_path = os.path.join(trading_directory, "secrets.json") # Arquivo das chaves

# Cria diretórios necessários
os.makedirs(trading_directory, exist_ok=True)
os.makedirs(os.path.join(trading_directory, "feature_importance_plots"), exist_ok=True)
os.makedirs(os.path.join(trading_directory, "confusion_matrix_plots"), exist_ok=True)
os.makedirs(os.path.join(trading_directory, "models"), exist_ok=True)

# --- Variáveis Globais de API ---
API_KEY = None
API_SECRET = None
client = None

# Chave de Criptografia (Deve ser fixa no .env para persistência)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    # Gera uma temporária se não houver (mas os dados serão perdidos ao reiniciar se não salvar no .env)
    print("AVISO: ENCRYPTION_KEY não encontrada no .env. Gerando chave temporária.")
    ENCRYPTION_KEY = Fernet.generate_key().decode()

cipher = Fernet(ENCRYPTION_KEY.encode())

def load_api_keys():
    """Tenta carregar chaves do .env ou do arquivo secrets.json"""
    global API_KEY, API_SECRET, client
    
    # 1. Tenta do .env
    env_key = os.getenv("API_KEY")
    env_secret = os.getenv("API_SECRET")
    
    if env_key and env_secret:
        API_KEY = env_key
        API_SECRET = env_secret
    # 2. Tenta do arquivo secrets.json
    elif os.path.exists(secrets_file_path):
        try:
            with open(secrets_file_path, 'r') as f:
                data = json.load(f)
                if 'api_key' in data and 'api_secret' in data:
                    API_KEY = cipher.decrypt(data['api_key'].encode()).decode()
                    API_SECRET = cipher.decrypt(data['api_secret'].encode()).decode()
        except Exception as e:
            print(f"Erro ao ler secrets.json: {e}")

    # Inicializa o cliente se tivermos chaves
    if API_KEY and API_SECRET:
        try:
            client = Client(API_KEY, API_SECRET)
            print("Cliente Binance inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar cliente Binance: {e}")
            client = None
    else:
        print("Chaves API não configuradas.")
        client = None

def save_api_keys(key, secret):
    """Salva as chaves criptografadas no arquivo"""
    try:
        encrypted_key = cipher.encrypt(key.encode()).decode()
        encrypted_secret = cipher.encrypt(secret.encode()).decode()
        
        with open(secrets_file_path, 'w') as f:
            json.dump({
                'api_key': encrypted_key,
                'api_secret': encrypted_secret
            }, f)
        
        # Recarrega na memória
        load_api_keys()
        return True
    except Exception as e:
        print(f"Erro ao salvar chaves: {e}")
        return False

# Carrega as chaves ao iniciar
load_api_keys()

# --- Parâmetros do Bot ---
TIMEFRAME = '15m'
TIMEFRAME_MAIOR = '1h'
TIMEFRAME_MACRO = '1d' 
# MIN_VOLUME_USDT = 50000000
MIN_VOLUME_USDT = 1000000 
ADX_THRESHOLD = 25 

log_file_path = os.path.join(trading_directory, "trading_log_v3.1.txt")
training_log_file_path = os.path.join(trading_directory, "training_melhoria_v3.1.txt")
plots_directory = os.path.join(trading_directory, "feature_importance_plots")
confusion_matrix_directory = os.path.join(trading_directory, "confusion_matrix_plots")
models_directory = os.path.join(trading_directory, "models")

# --- Gestão de Ativos ---
SYMBOL_BLACKLIST = [
    'SOLUSDT', 'ENAUSDT', 'PEPEUSDT', 'DOGEUSDT', 'SUIUSDT', '1000CHEEMSUSDT',
    'ADAUSDT', 'TRXUSDT', 'XRPUSDT', 'LTCUSDT', 'PAXGUSDT',
    'FDUSDUSDT', 'USDCUSDT', 'USDEUSDT'
]

CUSTOM_THRESHOLDS = {
    'BNBUSDT': 0.60,
}

# --- Configuração da Estratégia ---
STRATEGY_CONFIG = {
    'indicators': {
        'rsi': {'window': 14}, 'bollinger': {'window': 20, 'window_dev': 2},
        'ma_fast': {'window': 5}, 'ma_slow': {'window': 10},
        'ema_medium': {'window': 50}, 'ema_long': {'window': 200},
        'adx': {'window': 14}, 'atr': {'window': 14}, 'roc': {'periods': 5},
        'vol_of_vol': {'window': 20}, 'lags': {'rsi': 3}
    },
    'labeling': {
        'horizon_hours': 24, 'tp_atr_multiplier': 3.0, 'sl_atr_multiplier': 1.5
    },
    'regime_filter': { 
        'window': 50
    },
    'trailing_sl': {
        'atr_multiplier': 2.5
    }
}

# --- Lista de Features ---
ALL_FEATURES = [
    'RSI', 'MA_5', 'MA_10', 'EMA_50', 'EMA_200', 'adx', 'atr', 'volume', 
    'bb_bbm', 'bb_bbh', 'bb_bbl', 'dist_ema_200_pct', 'bb_width_pct', 
    'atr_pct', 'EMA_1h', 'day_of_week', 'hour_of_day', 'ema_50_roc', 
    'atr_pct_std_20', 'rsi_x_trend', 'rsi_lag'
]