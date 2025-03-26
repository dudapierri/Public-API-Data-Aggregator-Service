from flask import Flask, request, jsonify
import requests
import threading
from dotenv import load_dotenv
import os

load_dotenv()
CHAVE_API_OMDB = os.getenv("CHAVE_API_OMDB")
TOKEN_TMDB = os.getenv("TOKEN_TMDB")

app = Flask(__name__)


# buscar dados na OMDB título ano e sinopse
def buscar_dados_omdb(titulo, ano, resposta_final):
    url = f"http://www.omdbapi.com/?t={titulo}&y={ano}&apikey={CHAVE_API_OMDB}"
    resposta = requests.get(url)
    dados = resposta.json()
    if dados.get('Response') == "True":
        resposta_final['titulo'] = dados.get('Title', '')
        resposta_final['ano'] = int(dados.get('Year', 0))
        resposta_final['sinopse'] = dados.get('Plot', '')
    else:
        resposta_final['titulo'] = "*** Filme não encontrado ***"
        resposta_final['ano'] = None
        resposta_final['sinopse'] = ""


# buscar reviews no TMDB
def buscar_reviews_tmdb(titulo, resposta_final):
    cabecalho = {
        "Authorization": f"Bearer {TOKEN_TMDB}"
    }

    # buscar  id do filme
    url_busca = f"https://api.themoviedb.org/3/search/movie?query={titulo}&include_adult=false&language=pt-BR&page=1"
    resposta_busca = requests.get(url_busca, headers=cabecalho).json()
    id_filme = resposta_busca['results'][0]['id'] if resposta_busca.get('results') else None

    reviews = []
    if id_filme:
        # busca as reviews do filme
        url_reviews = f"https://api.themoviedb.org/3/movie/{id_filme}/reviews?language=pt-BR&page=1"
        resposta_reviews = requests.get(url_reviews, headers=cabecalho).json()
        for review in resposta_reviews.get('results', [])[:3]:
            reviews.append(review.get('content', ''))

    resposta_final['reviews'] = reviews

# rota principal da API
@app.route('/filme', methods=['POST'])
def processar_requisicao():
    dados_recebidos = request.get_json()
    titulo = dados_recebidos['titulo']
    ano = dados_recebidos['ano']

    resposta_final = {}

    # threads para buscar OMDB e TMDB ao mesmo tempo
    thread_omdb = threading.Thread(target=buscar_dados_omdb, args=(titulo, ano, resposta_final))
    thread_tmdb = threading.Thread(target=buscar_reviews_tmdb, args=(titulo, resposta_final))

    # inicia as threads
    thread_omdb.start()
    thread_tmdb.start()

    # aguarda as duas finalizarem
    thread_omdb.join()
    thread_tmdb.join()

    # retorna os dados agregados em JSON
    return jsonify(resposta_final)

# Inicia o servidor
if __name__ == '__main__':
    app.run(port=5000)
