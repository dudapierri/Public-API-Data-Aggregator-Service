#teste keys
import requests

CHAVE_API_OMDB = ""
TOKEN_TMDB = ""

titulo = "Interstellar"
ano = 2014

# Teste OMDB
def testar_omdb():
    print("Testando OMDB...")
    url = f"http://www.omdbapi.com/?t={titulo}&y={ano}&apikey={CHAVE_API_OMDB}"
    resposta = requests.get(url)
    if resposta.status_code == 200 and resposta.json().get('Response') == "True":
        print("OMDB funcionando!")
        print("Título:", resposta.json().get("Title"))
        print("Sinopse:", resposta.json().get("Plot"))
    else:
        print("Erro na OMDB:", resposta.json())

# Teste TMDB
def testar_tmdb():
    print("\nTestando TMDB...")
    headers = {
        "Authorization": f"Bearer {TOKEN_TMDB}"
    }
    url = f"https://api.themoviedb.org/3/search/movie?query={titulo}&language=pt-BR&page=1&include_adult=false"
    resposta = requests.get(url, headers=headers)
    if resposta.status_code == 200 and resposta.json().get("results"):
        print("TMDB funcionando!")
        print("Título encontrado:", resposta.json()["results"][0]["title"])
        print("ID do filme:", resposta.json()["results"][0]["id"])
    else:
        print("Erro na TMDB:", resposta.text)

if __name__ == "__main__":
    testar_omdb()
    testar_tmdb()