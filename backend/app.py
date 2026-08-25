from flask import Flask, jsonify, request
from flask_cors import CORS
from banco import (
    listar_filmes,
    buscar_filmes,
    filmes_melhor_avaliados,
    filmes_populares,
    buscar_filme_por_id,
    criar_review,
    listar_reviews_do_conteudo,
    buscar_review_do_usuario,
    atualizar_review,
    excluir_review,
    buscar_conteudo_por_tmdb_id
)
app = Flask(__name__)
CORS(app)


def transformar_filme(filme):
    return {
        "id": filme[0],
        "tmdb_id": filme[1],
        "titulo": filme[2],
        "titulo_original": filme[3],
        "tipo": filme[4],
        "sinopse": filme[5],
        "data_lancamento": filme[6],
        "nota_tmdb": filme[7],
        "popularidade": filme[8],
        "idioma": filme[9],
        "poster_path": filme[10],
        "generos": filme[11],
        "diretor": filme[12],
        "elenco": filme[13]
    }


@app.route("/api/filmes")
def filmes():
    resultados = listar_filmes()

    return jsonify([
        transformar_filme(filme)
        for filme in resultados
    ])


@app.route("/api/filmes/buscar")
def buscar():
    termo = request.args.get("q", "")

    resultados = buscar_filmes(termo)

    return jsonify([
        transformar_filme(filme)
        for filme in resultados
    ])


@app.route("/api/filmes/avaliados")
def avaliados():
    resultados = filmes_melhor_avaliados()

    return jsonify([
        transformar_filme(filme)
        for filme in resultados
    ])


@app.route("/api/filmes/populares")
def populares():
    resultados = filmes_populares()

    return jsonify([
        transformar_filme(filme)
        for filme in resultados
    ])


@app.route("/api/filmes/<int:tmdb_id>")
def filme_por_id(tmdb_id):

    filme = buscar_filme_por_id(tmdb_id)

    if filme is None:
        return jsonify({
            "erro": "Filme não encontrado"
        }), 404

    return jsonify(transformar_filme(filme))


# ==============================
# REVIEWS
# ==============================

@app.route("/api/conteudos/<int:tmdb_id>/reviews")
def reviews_do_conteudo(tmdb_id):

    conteudo_id = buscar_conteudo_por_tmdb_id(tmdb_id)

    print("TMDB ID:", tmdb_id)
    print("CONTEUDO ID ENCONTRADO:", conteudo_id)

    if conteudo_id is None:
        return jsonify({
            "erro": "Conteúdo não encontrado"
        }), 404

    reviews = listar_reviews_do_conteudo(conteudo_id)

    print("TMDB ID:", tmdb_id)
    print("CONTEUDO ID:", conteudo_id)
    print("REVIEWS ENCONTRADAS:", reviews)

    return jsonify([
        {
            "id": review[0],
            "user_id": review[1],
            "username": review[2],
            "nota": review[3],
            "texto": review[4],
            "created_at": review[5]
        }
        for review in reviews
    ])


@app.route("/api/conteudos/<int:conteudo_id>/reviews/usuario/<int:user_id>")

def review_do_usuario(conteudo_id, user_id):

    review = buscar_review_do_usuario(
        user_id,
        conteudo_id
    )

    if review is None:
        return jsonify(None)

    return jsonify({
        "id": review[0],
        "user_id": review[1],
        "conteudo_id": review[2],
        "nota": review[3],
        "texto": review[4],
        "created_at": review[5]
    })

@app.route("/api/conteudos/<int:tmdb_id>/reviews", methods=["POST"])
def criar_review_api(tmdb_id):

    dados = request.get_json()

    user_id = dados.get("user_id")
    nota = dados.get("nota")
    texto = dados.get("texto")
    if len(texto.strip()) > 1500:
        return jsonify({
            "erro": "A review pode ter no máximo 1500 caracteres."
        }), 400

    if not user_id or nota is None or not texto:
        return jsonify({
            "erro": "user_id, nota e texto são obrigatórios"
        }), 400

    if nota < 1 or nota > 10:
        return jsonify({
            "erro": "A nota deve estar entre 1 e 10"
        }), 400

    conteudo_id = buscar_conteudo_por_tmdb_id(tmdb_id)

    if conteudo_id is None:
        return jsonify({
            "erro": "Conteúdo não encontrado"
        }), 404

    sucesso = criar_review(
        user_id,
        conteudo_id,
        nota,
        texto
    )

    if not sucesso:
        return jsonify({
            "erro": "Esse usuário já possui uma review para esse conteúdo."
        }), 409

    return jsonify({
        "mensagem": "Review criada com sucesso!"
    }), 201

@app.route("/api/reviews/<int:review_id>", methods=["PUT"])
def editar_review_api(review_id):

    dados = request.get_json()

    nota = dados.get("nota")
    texto = dados.get("texto")

    if nota is None or not texto:
        return jsonify({
            "erro": "nota e texto são obrigatórios"
        }), 400

    if nota < 1 or nota > 10:
        return jsonify({
            "erro": "A nota deve estar entre 1 e 10"
        }), 400

    atualizar_review(
        review_id,
        nota,
        texto
    )

    return jsonify({
        "mensagem": "Review atualizada com sucesso!"
    })

@app.route("/api/reviews/<int:review_id>", methods=["DELETE"])
def deletar_review_api(review_id):

    excluir_review(review_id)

    return jsonify({
        "mensagem": "Review excluída com sucesso!"
    })

if __name__ == "__main__":
    app.run()
