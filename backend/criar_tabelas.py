import sys
import os

# Adiciona a pasta raiz ao path para encontrar o 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app, db

app = create_app()
with app.app_context():
    print("Conectando ao banco e criando tabelas...")
    db.create_all()
    print("Tabelas 'users', 'trades', 'open_positions' e 'bot_settings' criadas com sucesso!")