import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "cinelog.db")

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conteudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER UNIQUE,
            titulo TEXT NOT NULL,
            titulo_original TEXT,
            tipo TEXT NOT NULL,
            sinopse TEXT,
            data_lancamento TEXT,
            nota_tmdb REAL,
            popularidade REAL,
            idioma TEXT,
            poster_path TEXT
        )
    """)

    conexao.commit()
    conexao.close()

def inserir_conteudo(conteudo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO conteudos (
            tmdb_id,
            titulo,
            titulo_original,
            tipo,
            sinopse,
            data_lancamento,
            nota_tmdb,
            popularidade,
            idioma,
            poster_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        conteudo["tmdb_id"],
        conteudo["titulo"],
        conteudo["titulo_original"],
        conteudo["tipo"],
        conteudo["sinopse"],
        conteudo["data_lancamento"],
        conteudo["nota_tmdb"],
        conteudo["popularidade"],
        conteudo["idioma"],
        conteudo["poster_path"]
    ))

    conexao.commit()
    conexao.close()
def listar_filmes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM conteudos
        WHERE tipo = 'filme'
    """)

    filmes = cursor.fetchall()

    conexao.close()

    return filmes


def buscar_filmes(termo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM conteudos
        WHERE tipo = 'filme'
        AND titulo LIKE ?
    """, (f"%{termo}%",))

    filmes = cursor.fetchall()

    conexao.close()

    return filmes


def filmes_melhor_avaliados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM conteudos
        WHERE tipo = 'filme'
        ORDER BY nota_tmdb DESC
    """)

    filmes = cursor.fetchall()

    conexao.close()

    return filmes


def filmes_populares():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM conteudos
        WHERE tipo = 'filme'
        ORDER BY popularidade DESC
    """)

    filmes = cursor.fetchall()

    conexao.close()

    return filmes
if __name__ == "__main__":
    criar_tabela()

    filmes = filmes_populares()

    print("Filmes mais populares:")

    for filme in filmes:
        print(f"{filme[2]} - Popularidade: {filme[8]}")