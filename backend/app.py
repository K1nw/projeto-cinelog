import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ARQUIVO_BANCO = os.path.join(os.path.dirname(__file__), 'filmes.json')

def carregar_filmes():
    if not os.path.exists(ARQUIVO_BANCO):
        filmes_iniciais = [
            {"id": 1, "titulo": "Interestelar", "nota": 9.5, "review": "Uma obra-prima."},
            {"id": 2, "titulo": "Matrix", "nota": 9.0, "review": "Revolucionário."}
        ]
        salvar_filmes(filmes_iniciais)
        return filmes_iniciais

    with open(ARQUIVO_BANCO, 'r', encoding='utf-8') as f:
        filmes = json.load(f)

    precisa_atualizar = False
    maior_id = 0

    for filme in filmes:
        if "id" in filme and filme["id"] > maior_id:
            maior_id = filme["id"]

    for filme in filmes:
        if "id" not in filme:
            maior_id += 1
            filme["id"] = maior_id
            precisa_atualizar = True
    if precisa_atualizar:
        salvar_filmes(filmes)

    return filmes
def salvar_filmes(dados):
    with open(ARQUIVO_BANCO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route('/api/filmes', methods=['GET'])
def obter_filmes():
    filmes = carregar_filmes()
    return jsonify(filmes)

@app.route('/api/filmes', methods=['POST'])
def adicionar_filme():
    dados = request.get_json()

    if not dados or 'titulo' not in dados:
        return jsonify({"erro": "Título é obrigatório"}), 400

    filmes = carregar_filmes()

    novo_id = 1
    if filmes:
        novo_id = max(filme["id"] for filme in filmes) + 1

    novo_filme = {
        "id": novo_id,
        "titulo": dados.get("titulo"),
        "nota": dados.get("nota", 0),
        "review": dados.get("review", "")
    }

    filmes.append(novo_filme)
    salvar_filmes(filmes)

    return jsonify(novo_filme), 201

@app.route('/api/filmes/<int:id>', methods=['DELETE'])
def deletar_filme(id):
    filmes = carregar_filmes()

    filme_encontrado = None
    for filme in filmes:
        if filme["id"] == id:
            filme_encontrado = filme
            break

    if filme_encontrado is None:
        return jsonify({"erro": "Filme não encontrado"}), 404

    filmes.remove(filme_encontrado)
    salvar_filmes(filmes)

    return jsonify({"mensagem": "Filme deletado com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)