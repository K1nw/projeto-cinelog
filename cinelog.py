import json

filmes = []

def mostrar_menu():
    print("=== CineLog ===")
    print("1 - Adicionar Filmes")
    print("2 - Listar Filmes")
    print("3 - Sair")
def salvar_filmes():
    with open("filmes.json", "w", encoding="utf-8") as arquivo:
        json.dump(filmes, arquivo, ensure_ascii=False, indent=4)
def adicionar_filme():
    filme = {}
    filme["titulo"] = input("Título do filme: ")

    while True:
        nota = float(input("Nota (1 a 10): "))
        if 1 <= nota <= 10:
            filme["nota"] = nota
            break
        else:
            print("Nota inválida. Digite um número de 1 a 10.")

    filme["review"] = input("Review: ")
    filmes.append(filme)
    salvar_filmes()   
    print("Filme adicionado com sucesso!")
def listar_filmes():
    if len(filmes) == 0:
        print("Nenhum filme cadastrado.")
    else:
        for filme in filmes:
            print(f"Título: {filme['titulo']}")
            print(f"Nota: {filme['nota']}")
            print(f"Review: {filme['review']}")
            print("-" * 20)
def carregar_filmes():
    global filmes
    try:
        with open("filmes.json", "r", encoding="utf-8") as arquivo:
            filmes = json.load(arquivo)
    except FileNotFoundError:
        filmes = []
carregar_filmes()
while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_filme()
    elif opcao == "2":
        listar_filmes()
    elif opcao == "3":
        print("Saindo do CineLog...")
        break
    else:
        print("Opção inválida.")