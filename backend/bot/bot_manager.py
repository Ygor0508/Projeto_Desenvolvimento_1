# import threading
# import time
# from .core import TradingBot
# from flask import current_app

# class BotManager:
#     def __init__(self):
#         self.bot_thread = None
#         self.bot_instance = None
#         self.is_running = False

#     def start_bot(self, user_id):
#         if self.is_running:
#             return False, "O bot já está em execução."

#         self.is_running = True
#         self.bot_instance = TradingBot(user_id)
        
#         app_context = current_app.app_context()
#         self.bot_thread = threading.Thread(target=self.run_bot_with_context, args=(self.bot_instance, app_context))
#         self.bot_thread.start()
#         return True, "Bot iniciado com sucesso."

#     def stop_bot(self):
#         if not self.is_running or not self.bot_instance:
#             return False, "O bot não está em execução."

#         self.bot_instance.stop()
#         self.bot_thread.join()
#         self.is_running = False
#         self.bot_instance = None
#         self.bot_thread = None
#         return True, "Bot parado com sucesso."

#     def get_status(self, user_id):
#         if not self.is_running or not self.bot_instance:
#             return {"status": "Parado", "user_id": user_id}
#         if self.bot_instance.user.id == user_id:
#             return self.bot_instance.get_status()
#         return {"status": "Parado", "user_id": user_id, "error": "Bot em execução para outro usuário."}

#     def run_bot_with_context(self, bot_instance, app_context):
#         with app_context:
#             bot_instance.run()

# bot_manager = BotManager()






# backend/bot/bot_manager.py
import threading
import time
import os
import joblib
from backend.config import models_directory

# --- Estado Global do Bot ---
bot_running = False
MODELS_AND_REGIME = {} # {symbol: (model, scaler, is_bullish)}
CURRENT_POSITIONS = {} # {symbol: {dados_posicao}}
LOCK = threading.Lock()

def load_models_disk():
    print("Carregando modelos do disco...")
    data = {}
    try:
        if not os.path.exists(models_directory):
            print("Diretório de modelos não encontrado.")
            return

        for f in os.listdir(models_directory):
            if f.endswith("_model.joblib"):
                sym = f.replace("_model.joblib", "")
                m = joblib.load(os.path.join(models_directory, f))
                s = joblib.load(os.path.join(models_directory, f"{sym}_scaler.joblib"))
                data[sym] = (m, s, False) # Regime padrão False até atualizar
        update_models(data)
    except Exception as e:
        print(f"Erro loading models: {e}")

def update_models(new_data):
    global MODELS_AND_REGIME
    with LOCK: MODELS_AND_REGIME = new_data
    print("Modelos atualizados na memória.")

def get_position(symbol):
    with LOCK: return CURRENT_POSITIONS.get(symbol)

def update_position(symbol, data):
    global CURRENT_POSITIONS
    with LOCK:
        if data is None: 
            if symbol in CURRENT_POSITIONS: del CURRENT_POSITIONS[symbol]
        else: CURRENT_POSITIONS[symbol] = data

def trading_loop():
    # Importação Tardia para evitar Ciclo
    import backend.bot.core as core
    
    print("Loop de trading iniciado.")
    while bot_running:
        with LOCK: models = MODELS_AND_REGIME.copy()
        
        if not models:
            print("Sem modelos. Aguardando...")
            time.sleep(10)
            continue
            
        for symbol, (model, scaler, regime) in models.items():
            if not bot_running: break
            try:
                core.check_symbol_logic(symbol, model, scaler, regime)
            except Exception as e:
                print(f"Erro no loop {symbol}: {e}")
        
        # Pausa entre ciclos
        time.sleep(10)

def start_bot():
    # Importações Tardias para evitar Ciclo
    import backend.bot.training_manager as tm 

    global bot_running
    if bot_running: return
    bot_running = True
    
    load_models_disk()
    threading.Thread(target=trading_loop, daemon=True).start()
    threading.Thread(target=tm.start_training_scheduler, daemon=True).start()
    
    # Inicia um treino imediato em background se não tiver modelos
    if not MODELS_AND_REGIME:
        print("Iniciando primeiro treinamento...")
        threading.Thread(target=tm.run_full_training_cycle, daemon=True).start()

def stop_bot():
    global bot_running
    bot_running = False