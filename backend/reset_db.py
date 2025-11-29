import sys
import os

# Adiciona a pasta raiz ao caminho para importar o backend corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
from backend.models import db

def reset_db():
    print("🔄 Conectando ao Banco de Dados...")
    with app.app_context():
        # 1. Destrói tudo o que existe (Limpeza Total)
        print("🗑️  Apagando tabelas antigas...")
        db.drop_all()
        
        # 2. Cria as tabelas novas baseadas no models.py atualizado
        print("✨ Criando novas tabelas (com colunas de risco e trade_amount)...")
        db.create_all()
        
        print("✅ Sucesso! Banco de dados atualizado.")

if __name__ == "__main__":
    reset_db()