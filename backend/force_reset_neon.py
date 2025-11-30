# backend/force_reset_neon.py
import sys
import os

# Adiciona a pasta raiz ao sistema para importar o backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
from backend.models import db

# SUA URL DO NEON (Copiada dos seus dados)
NEON_URL = "postgresql://neondb_owner:npg_xFJ7Ldg6wbXY@ep-calm-block-a4utcnyf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def force_reset():
    print(f"🔌 Conectando ao Banco Neon na Nuvem...")
    
    # Força a aplicação a usar o banco Neon agora
    app.config['SQLALCHEMY_DATABASE_URI'] = NEON_URL
    
    with app.app_context():
        print("🗑️  Apagando tabelas antigas (DROP)...")
        db.drop_all()
        
        print("✨ Criando novas tabelas com campos de Risco (CREATE)...")
        db.create_all()
        
        print("✅ SUCESSO! O Banco de Dados Neon foi atualizado.")

if __name__ == "__main__":
    force_reset()