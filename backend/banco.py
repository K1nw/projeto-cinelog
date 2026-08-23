import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "cinelog.db")

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def criar_banco():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS conteudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            titulo_original TEXT,
            tipo TEXT NOT NULL,
            ano_inicio INTEGER,
            ano_fim INTEGER,
            sinopse TEXT,
            poster TEXT,
            nota_media REAL DEFAULT 0
        )
    """)

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()
    print("Banco criado com sucesso.")