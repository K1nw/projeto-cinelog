import json
filmes = []

def mostrar_menu():
    print("=== CineLog ===")
    print("1 - Adicionar Filmes")
    print("2 - Listar Filmes")
    print("3 - Editar Filmes")
    print("4 - Excluir Filmes")
    print("5 - Sair")

#função de arquivo
def salvar_filmes():
    with open("filmes.json", "w", encoding="utf-8") as arquivo:
        json.dump(filmes, arquivo, ensure_ascii=False, indent=4)

#funções de sistema
def adicionar_filme():
    filme = {}

    filme["titulo"] = input("Título do filme ( 0 para voltar ): ")
    if filme["titulo"] == "0":
        return
    
    while True:
        try:
            nota = float(input("Nota (1 a 10) ou 0 para voltar : "))

            if nota == 0:
                return

            if 1 <= nota <= 10:
                filme["nota"] = nota
                break
            else:
                print("Nota inválida.")
        except ValueError:
            print("Digite apenas números.")
    filme["review"] = input("Review: ")
    filmes.append(filme)
    salvar_filmes()
    print("Filme adicionado com sucesso!")

def listar_filmes():
    if not filmes:
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

def editar_filme():
    if not filmes:
        print("Nenhum filme para editar")
        return
    print("Escolha o Número do filme que deseja Editar:")
    print("0 - voltar")
    for numero, filme in enumerate(filmes, start=1):
        print(f"{numero} - {filme['titulo']}")
    
    opcao = int(input("Digite o número do filme: "))
    if opcao == 0:
        return
    filme = filmes[opcao - 1]
    print(f"Título: {filme['titulo']}")
    print(f"Nota: {filme['nota']}")
    print(f"Review: {filme['review']}")
    campo = input("Deseja alterar o titulo, nota ou review?: ").lower()
    if campo not in ["titulo", "nota", "review"]:
        print("Digite uma opção válida.")
        return
    if campo == "titulo":
        novo_titulo = input("Novo título: ")
        filme["titulo"] = novo_titulo
    elif campo == "nota":
        nova_nota = float(input("Nova nota: "))
        filme["nota"] = nova_nota
    elif campo == "review":
        novo_review = input("Nova review: ")
        filme["review"] = novo_review
    with open("filmes.json", "w", encoding="utf-8") as arquivo:
        json.dump(filmes, arquivo, ensure_ascii=False, indent=4)

def excluir_filme():
    if not filmes:
        print("Nenhum filme para excluir.")
        return
    print("Escolha o Número do filme que deseja excluir:")
    print("0 - Voltar")
    for numero, filme in enumerate(filmes, start=1):
        print(f"{numero} - {filme['titulo']}")
    opcao = int(input("Digite o número do filme para excluir: "))
    if opcao == 0:
        return
    filme = filmes[opcao - 1]
    print(f"Deseja mesmo excluir o filme: {filme['titulo']} (número {opcao})? s/n")
    confirmar = input().strip().lower()
    if confirmar not in ['s', 'y', 'sim', 'yes']:
        print("Exclusão cancelada.")
        return
    filmes.pop(opcao - 1)
    salvar_filmes()
    print("Filme excluído com sucesso!")

# Menu principal
while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_filme()
    elif opcao == "2":
        listar_filmes()
    elif opcao == "3":
        editar_filme()
    elif opcao == "4":
        print("Excluir filmes")
        excluir_filme()
    elif opcao == "5":
        print("Saindo do Cinelog")
        break
    else:
        print("Opção inválida.")