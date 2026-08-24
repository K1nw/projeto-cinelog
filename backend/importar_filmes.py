import os
import json
import requests

from dotenv import load_dotenv

from banco import (
    criar_tabela,
    atualizar_tabela,
    inserir_conteudo,
    atualizar_conteudo
)

load_dotenv()

token = os.getenv("TMDB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}

url_populares = "https://api.themoviedb.org/3/movie/popular"


def buscar_detalhes_filme(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

    parametros = {
        "append_to_response": "credits"
    }

    resposta = requests.get(
        url,
        headers=headers,
        params=parametros
    )

    if not resposta.ok:
        print(
            f"Erro ao buscar detalhes do filme {tmdb_id}: "
            f"{resposta.status_code}"
        )
        return None

    return resposta.json()


criar_tabela()
atualizar_tabela()

resposta = requests.get(
    url_populares,
    headers=headers
)

print("Status:", resposta.status_code)

if resposta.ok:

    dados = resposta.json()

    for filme in dados["results"][:10]:

        detalhes = buscar_detalhes_filme(filme["id"])

        if detalhes is None:
            continue

        generos = [
            genero["name"]
            for genero in detalhes.get("genres", [])
        ]

        diretor = ""

        for pessoa in detalhes.get("credits", {}).get("crew", []):
            if pessoa.get("job") == "Director":
                diretor = pessoa.get("name", "")
                break

        elenco = []

        for pessoa in detalhes.get("credits", {}).get("cast", [])[:10]:

            elenco.append({
                "id": pessoa.get("id"),
                "nome": pessoa.get("name"),
                "personagem": pessoa.get("character"),
                "foto": pessoa.get("profile_path")
            })

        conteudo = {
            "tmdb_id": filme["id"],
            "titulo": filme["title"],
            "titulo_original": filme["original_title"],
            "tipo": "filme",
            "sinopse": filme["overview"],
            "data_lancamento": filme["release_date"],
            "nota_tmdb": filme["vote_average"],
            "popularidade": filme["popularity"],
            "idioma": filme["original_language"],
            "poster_path": filme["poster_path"],

            "generos": ", ".join(generos),
            "diretor": diretor,
            "elenco": json.dumps(
                elenco,
                ensure_ascii=False
            )
        }

        inserir_conteudo(conteudo)

        atualizar_conteudo(conteudo)

        print(
            f"Importado: {filme['title']} "
            f"| Diretor: {diretor} "
            f"| Gêneros: {', '.join(generos)} "
            f"| Elenco: {len(elenco)}"
        )

else:

    print("Erro:", resposta.text)