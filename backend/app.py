from flask import Flask, jsonify, request
from flask_cors import CORS
from banco import (
    listar_filmes,
    buscar_filmes,
    filmes_melhor_avaliados,
    filmes_populares,
    buscar_filme_por_id
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

if __name__ == "__main__":
    app.run()