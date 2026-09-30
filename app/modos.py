MODOS = {
    "1": {
        "nome": "LEITURA DE 3 SÍMBOLOS",
        "descricao": "Passado, presente e caminho."
    },
    "2": {
        "nome": "PERGUNTA DIRETA",
        "descricao": "Uma leitura simbólica focada numa pergunta."
    },
    "3": {
        "nome": "MENSAGEM DO MOMENTO",
        "descricao": "Uma mensagem simbólica sem pergunta específica."
    },
    "4": {
        "nome": "EXPLORAÇÃO",
        "descricao": "Uma leitura aberta para reflexão."
    }
}


def mostrar_menu():
    print()
    print("┌──────────────────────────────┐")
    print("│        OLHO DE DEUS          │")
    print("├──────────────────────────────┤")

    for numero, modo in MODOS.items():
        print(f"│  {numero}. {modo['nome']:<25}│")

    print("│  0. SAIR                     │")
    print("└──────────────────────────────┘")
    print()


def obter_modo():
    while True:
        mostrar_menu()
        escolha = input("Escolha o modo: ").strip()

        if escolha.lower() in ("0", "sair", "exit", "quit"):
            return None

        if escolha in MODOS:
            return MODOS[escolha]

        print("\nOpção inválida. Escolha 1, 2, 3, 4 ou 0.\n")
