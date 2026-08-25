import sqlite3
import os

# Caminho do banco (fica na mesma pasta do arquivo)
CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "cinelog.db")

def conectar():
    """Abre conexão com o banco"""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


# ==============================
# TABELA DE CONTEÚDOS
# ==============================

def criar_tabela():
    """Cria a tabela principal de conteúdos (filmes, séries, animes)"""
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
    """Insere um conteúdo novo. Se já existir (mesmo tmdb_id), ignora."""
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

def atualizar_conteudo(conteudo):
    """Atualiza os dados de um conteúdo que já existe no banco"""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE conteudos
        SET
            titulo = ?,
            titulo_original = ?,
            sinopse = ?,
            data_lancamento = ?,
            nota_tmdb = ?,
            popularidade = ?,
            idioma = ?,
            poster_path = ?,
            generos = ?,
            diretor = ?,
            elenco = ?
        WHERE tmdb_id = ?
    """, (
        conteudo["titulo"],
        conteudo["titulo_original"],
        conteudo["sinopse"],
        conteudo["data_lancamento"],
        conteudo["nota_tmdb"],
        conteudo["popularidade"],
        conteudo["idioma"],
        conteudo["poster_path"],
        conteudo["generos"],
        conteudo["diretor"],
        conteudo["elenco"],
        conteudo["tmdb_id"]
    ))

    conexao.commit()
    conexao.close()

# ==============================
# BUSCA DE CONTEÚDOS
# ==============================

def listar_filmes():
    """Retorna todos os filmes cadastrados"""
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

def buscar_filme_por_id(tmdb_id):
    """Busca um filme específico pelo ID do TMDB"""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM conteudos
        WHERE tipo = 'filme'
        AND tmdb_id = ?
    """, (tmdb_id,))

    filme = cursor.fetchone()

    conexao.close()

    return filme

def buscar_filmes(termo):
    """Busca filmes pelo título (pesquisa parcial)"""
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
    """Retorna os filmes ordenados pela nota do TMDB (maior pra menor)"""
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
    """Retorna os filmes ordenados por popularidade"""
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

def buscar_conteudo_por_tmdb_id(tmdb_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id
        FROM conteudos
        WHERE tmdb_id = ?
    """, (tmdb_id,))

    resultado = cursor.fetchone()

    conexao.close()

    return resultado[0] if resultado else None


# ==============================
# ATUALIZAÇÃO DA TABELA
# ==============================


def atualizar_tabela():
    """Adiciona colunas novas na tabela se elas ainda não existirem.
    Útil quando a gente vai evoluindo o banco sem quebrar o que já tem."""
    conexao = conectar()
    cursor = conexao.cursor()

    colunas = [
        ("generos", "TEXT"),
        ("diretor", "TEXT"),
        ("elenco", "TEXT")
    ]

    for nome, tipo in colunas:
        try:
            cursor.execute(
                f"ALTER TABLE conteudos ADD COLUMN {nome} {tipo}"
            )
        except sqlite3.OperationalError:
            # Coluna já existe, só ignora
            pass

    conexao.commit()
    conexao.close()

# ==============================
# TABELA DE USUÁRIOS
# ==============================

def criar_tabela_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )

""")
    conexao.commit()
    conexao.close()

# ==============================
# FUNÇÕES DE USUÁRIOS
# ==============================

def criar_usuario(username, password):
    """Cria um novo usuário no CineLog"""

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        conexao.commit()

        print(f"Usuário '{username}' criado com sucesso!")

    except sqlite3.IntegrityError:
        print(f"O usuário '{username}' já existe.")

    finally:
        conexao.close()


def listar_usuarios():
    """Retorna todos os usuários cadastrados"""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, username, created_at
        FROM users
        ORDER BY id
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    return usuarios

# ==============================
# FUNÇÕES DE REVIEWS
# ==============================

def criar_review(user_id, conteudo_id, nota, texto):
    """Cria uma nova review para um conteúdo"""

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            INSERT INTO reviews (
                user_id,
                conteudo_id,
                nota,
                texto
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            conteudo_id,
            nota,
            texto
        ))

        conexao.commit()

        print("Review criada com sucesso!")

        return True

    except sqlite3.IntegrityError:

        print("Esse usuário já possui uma review para esse conteúdo.")

        return False

    finally:
        conexao.close()


def listar_reviews_do_conteudo(conteudo_id):
    """Retorna todas as reviews de um conteúdo"""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT
        reviews.id,
        reviews.user_id,
        users.username,
        reviews.nota,
        reviews.texto,
        reviews.created_at
    FROM reviews
    INNER JOIN users
        ON reviews.user_id = users.id
    WHERE reviews.conteudo_id = ?
    ORDER BY reviews.created_at DESC
""", (conteudo_id,))

    reviews = cursor.fetchall()

    conexao.close()

    return reviews




# ==============================
# TABELA DE REVIEWS
# ==============================

def criar_tabela_reviews():
    """Cria a tabela de reviews dos usuários"""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            conteudo_id INTEGER NOT NULL,
            nota INTEGER NOT NULL,
            texto TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id)

        )
    """)
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_review_usuario_conteudo
    ON reviews (user_id, conteudo_id)
    """)

    conexao.commit()
    conexao.close()

def buscar_review_do_usuario(user_id, conteudo_id):
    """Busca a review de um usuário para um conteúdo específico"""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            conteudo_id,
            nota,
            texto,
            created_at
        FROM reviews
        WHERE user_id = ?
        AND conteudo_id = ?
    """, (user_id, conteudo_id))

    review = cursor.fetchone()

    conexao.close()

    return review

def atualizar_review(review_id, nota, texto):
    """Atualiza a nota e o texto de uma review"""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE reviews
        SET
            nota = ?,
            texto = ?
        WHERE id = ?
    """, (
        nota,
        texto,
        review_id
    ))

    conexao.commit()

    if cursor.rowcount > 0:
        print("Review atualizada com sucesso!")
    else:
        print("Review não encontrada.")

    conexao.close()

def excluir_review(review_id):
    """Exclui uma review pelo ID"""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM reviews
        WHERE id = ?
    """, (review_id,))

    conexao.commit()

    if cursor.rowcount > 0:
        print("Review excluída com sucesso!")
    else:
        print("Review não encontrada.")

    conexao.close()

reviews = listar_reviews_do_conteudo(1)

print("\nReviews do Spider-Man:")




for review in reviews:
    print(
        f"ID: {review[0]} | "
        f"Usuário: {review[1]} | "
        f"Nota: {review[2]}/10 | "
        f"Review: {review[3]}"
    )

print("\nTODAS AS REVIEWS:")

conexao = conectar()
cursor = conexao.cursor()

cursor.execute("""
    SELECT
        reviews.id,
        reviews.user_id,
        users.username,
        reviews.conteudo_id,
        reviews.nota,
        reviews.texto
    FROM reviews
    INNER JOIN users ON reviews.user_id = users.id
    ORDER BY reviews.id
""")

for review in cursor.fetchall():
    print(review)


# Só roda quando executar o arquivo diretamente
if __name__ == "__main__":
    criar_tabela()
    atualizar_tabela()
    criar_tabela_usuarios()
    criar_tabela_reviews()

    criar_usuario("Ana", "teste001")
    criar_usuario("Bruno", "teste002")
    criar_usuario("Camila", "teste003")
    criar_usuario("Diego", "teste004")
    criar_usuario("Eduarda", "teste005")
    criar_usuario("Felipe", "teste006")
    criar_usuario("Gabriel", "teste007")
    criar_usuario("Helena", "teste008")
    criar_usuario("Igor", "teste009")
    criar_usuario("Larissa", "teste010")

    usuarios = listar_usuarios()
    print("\nUsuários cadastrados:")

    for usuario in usuarios:
        print(f"ID: {usuario[0]} | Usuário: {usuario[1]} | Criado em: {usuario[2]}")

    filmes = filmes_populares()

    print("\nFilmes mais populares:")

    for filme in filmes:
        print(f"{filme[2]} - Popularidade: {filme[8]}")

conexao = conectar()
cursor = conexao.cursor()

cursor.execute("""
    SELECT id, tmdb_id, titulo
    FROM conteudos
    WHERE tmdb_id = 1323244
""")

print(cursor.fetchall())

conexao.close()
