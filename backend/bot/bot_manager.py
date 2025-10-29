import threading
import time
from .core import TradingBot
from flask import current_app

class BotManager:
    def __init__(self):
        self.bot_thread = None
        self.bot_instance = None
        self.is_running = False

    def start_bot(self, user_id):
        if self.is_running:
            return False, "O bot já está em execução."

        self.is_running = True
        self.bot_instance = TradingBot(user_id)
        
        app_context = current_app.app_context()
        self.bot_thread = threading.Thread(target=self.run_bot_with_context, args=(self.bot_instance, app_context))
        self.bot_thread.start()
        return True, "Bot iniciado com sucesso."

    def stop_bot(self):
        if not self.is_running or not self.bot_instance:
            return False, "O bot não está em execução."

        self.bot_instance.stop()
        self.bot_thread.join()
        self.is_running = False
        self.bot_instance = None
        self.bot_thread = None
        return True, "Bot parado com sucesso."

    def get_status(self, user_id):
        if not self.is_running or not self.bot_instance:
            return {"status": "Parado", "user_id": user_id}
        if self.bot_instance.user.id == user_id:
            return self.bot_instance.get_status()
        return {"status": "Parado", "user_id": user_id, "error": "Bot em execução para outro usuário."}

    def run_bot_with_context(self, bot_instance, app_context):
        with app_context:
            bot_instance.run()

bot_manager = BotManager()

