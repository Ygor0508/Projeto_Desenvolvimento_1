# from backend import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)





# # run.py
# import time
# from backend.app import app
# from backend.bot.bot_manager import start_bot, stop_bot
# import threading

# def run_flask():
#     # Roda o Flask na porta 5000
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# if __name__ == '__main__':
#     print("Iniciando Sistema...")
    
#     # Inicia o Flask em uma thread separada para não bloquear o robô
#     flask_thread = threading.Thread(target=run_flask, daemon=True)
#     flask_thread.start()
    
#     # Inicia o Robô
#     start_bot()
    
#     try:
#         while True: time.sleep(1)
#     except KeyboardInterrupt:
#         print("Parando...")
#         stop_bot()








# # run.py
# import time
# import threading
# from backend.app import app
# from backend.models import db # Importa o banco para criar as tabelas
# from backend.bot.bot_manager import start_bot, stop_bot

# def run_flask():
#     # Roda o Flask na porta 5000
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# def initialize_database():
#     """
#     Função de Auto-Correção:
#     Cria as tabelas no banco de dados automaticamente ao iniciar o sistema.
#     Isso resolve o problema de não ter acesso ao Shell do Render.
#     """
#     print("🛠️  VERIFICANDO BANCO DE DADOS NA NUVEM...")
#     try:
#         with app.app_context():
#             db.create_all() # Cria todas as tabelas definidas no models.py se não existirem
#         print("✅ Banco de Dados verificado e atualizado com sucesso!")
#     except Exception as e:
#         print(f"❌ Erro ao atualizar banco de dados: {e}")

# if __name__ == '__main__':
#     print("🚀 Iniciando Sistema de Trading...")
    
#     # 1. O Pulo do Gato: Atualiza o banco ANTES de ligar o robô
#     initialize_database()
    
#     # 2. Inicia o Site (API) em background
#     flask_thread = threading.Thread(target=run_flask, daemon=True)
#     flask_thread.start()
    
#     # 3. Inicia o Robô
#     start_bot()
    
#     try:
#         # Mantém o programa rodando
#         while True: 
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Parando o sistema...")
#         stop_bot()







# # run.py
# import time
# import threading
# from backend.app import app
# from backend.models import db
# from backend.bot.bot_manager import start_bot, stop_bot
# import backend.config as config # Importa config para carregar chaves

# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# def initialize_system():
#     print("🛠️  VERIFICANDO SISTEMA NA NUVEM...")
#     try:
#         with app.app_context():
#             # 1. Cria tabelas se não existirem
#             db.create_all()
#             print("✅ Banco de Dados verificado.")
            
#             # 2. Tenta carregar chaves salvas no banco
#             print("🔑 Tentando carregar chaves API...")
#             if config.load_from_db():
#                 print("✅ Chaves carregadas! Robô pronto.")
#             else:
#                 print("⚠️ Nenhuma chave encontrada. Configure no painel.")
                
#     except Exception as e:
#         print(f"❌ Erro na inicialização: {e}")

# if __name__ == '__main__':
#     print("🚀 Iniciando Sistema de Trading...")
    
#     # Inicializa Banco e Chaves
#     initialize_system()
    
#     flask_thread = threading.Thread(target=run_flask, daemon=True)
#     flask_thread.start()
    
#     start_bot()
    
#     try:
#         while True: time.sleep(1)
#     except KeyboardInterrupt:
#         stop_bot()








# # run.py
# import time
# import threading
# from backend.app import app
# from backend.models import db
# from backend.bot.bot_manager import start_bot, stop_bot
# import backend.config as config

# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# def initialize_system():
#     print("🛠️  VERIFICANDO SISTEMA NA NUVEM...")
#     with app.app_context():
#         try:
#             # Tenta criar tabelas
#             db.create_all()
#             print("✅ Tabelas verificadas/criadas.")
#         except Exception as e:
#             print(f"❌ Erro crítico ao criar tabelas: {e}")
            
#         try:
#             # Tenta carregar chaves
#             if config.load_from_db():
#                 print("✅ Chaves carregadas.")
#             else:
#                 print("⚠️ Sem chaves.")
#         except Exception as e:
#             print(f"❌ Erro ao carregar chaves: {e}")

# if __name__ == '__main__':
#     print("🚀 Iniciando...")
#     initialize_system()
    
#     flask_thread = threading.Thread(target=run_flask, daemon=True)
#     flask_thread.start()
    
#     start_bot()
    
#     try:
#         while True: time.sleep(1)
#     except KeyboardInterrupt:
#         stop_bot()









import time
import threading
from waitress import serve
from backend.app import app
from backend.models import db
from backend.bot.bot_manager import start_bot, stop_bot
import backend.config as config

def initialize_system():
    """Garante que tabelas e chaves existam antes de iniciar"""
    print("🛠️  VERIFICANDO SISTEMA NA NUVEM...")
    with app.app_context():
        try:
            # Tenta criar tabelas
            db.create_all()
            print("✅ Tabelas verificadas/criadas.")
        except Exception as e:
            print(f"❌ Erro crítico ao criar tabelas: {e}")
            
        try:
            # Tenta carregar chaves
            if config.load_from_db():
                print("✅ Chaves carregadas.")
            else:
                print("⚠️ Sem chaves configuradas.")
        except Exception as e:
            print(f"❌ Erro ao carregar chaves: {e}")

def start_server():
    """Inicia o servidor web Waitress em background"""
    print("🌍 Iniciando Servidor Web Profissional (Waitress) na porta 5000...")
    # 'threads=6' garante que o site responda mesmo se o robô estiver ocupado
    serve(app, host='0.0.0.0', port=5000, threads=6)

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Trading Completo...")
    
    # 1. Configuração Inicial
    initialize_system()
    
    # 2. Inicia o Site (API) em uma thread separada
    # daemon=True significa que se o programa principal fechar, o site fecha junto
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 3. Inicia o Robô (O BotManager gerencia a thread interna dele)
    print("🤖 Ligando motor do robô...")
    start_bot()
    
    print("✅ Sistema Operacional! Aguardando comandos...")
    
    try:
        # Loop principal que mantém o programa vivo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Parando sistema...")
        stop_bot()