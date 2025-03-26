import requests
def main():
    print("-----------------")
    print("Consulta de Filme")
    print("Aluna: Maria Eduarda Pierri")
    print("------------------")

    # solicita entrada do usuário
    titulo = input("Digite o título do filme: ")
    ano = int(input("Digite o ano do filme: "))
    print("------------------")

    dados_envio = {
        "titulo": titulo,
        "ano": ano
    }

    # envia requisição POST para o servidor
    resposta = requests.post("http://localhost:5000/filme", json=dados_envio)

    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        dados = resposta.json()
        print("\n------------------")
        print("Resultado")
        print("------------------")
        print(f"Título: {dados.get('titulo')}")
        print(f"Ano: {dados.get('ano')}")
        print(f"Sinopse: {dados.get('sinopse')}\n")
        print("Reviews:")
        for i, review in enumerate(dados.get('reviews', []), start=1):
            print(f"{i}. {review}\n")
    else:
        print("Erro ao buscar informações do filme")


if __name__ == "__main__":
    main()
