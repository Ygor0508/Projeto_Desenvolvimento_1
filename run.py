# from backend import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# run.py
import time
from backend.app import app
from backend.bot.bot_manager import start_bot, stop_bot
import threading

def run_flask():
    # Roda o Flask na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("Iniciando Sistema...")
    
    # Inicia o Flask em uma thread separada para não bloquear o robô
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Inicia o Robô
    start_bot()
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("Parando...")
        stop_bot()