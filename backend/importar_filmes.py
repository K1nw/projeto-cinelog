import os
import requests
from dotenv import load_dotenv
from banco import criar_tabela, inserir_conteudo

load_dotenv()

token = os.getenv("TMDB_TOKEN")

url = "https://api.themoviedb.org/3/movie/popular"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}

criar_tabela()

resposta = requests.get(url, headers=headers)

print("Status:", resposta.status_code)

if resposta.ok:
    dados = resposta.json()

    for filme in dados["results"][:10]:
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
            "poster_path": filme["poster_path"]
        }

        inserir_conteudo(conteudo)

        print(f"Importado: {filme['title']}")

else:
    print("Erro:", resposta.text)