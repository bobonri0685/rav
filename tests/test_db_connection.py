import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app, db

with app.app_context():
    try:
        # Obtém uma conexão do engine e executa uma consulta simples
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Conexão com o banco de dados bem-sucedida.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
