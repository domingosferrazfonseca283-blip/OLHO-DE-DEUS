from oraculo import consultar, obter_historico
from interpretador import interpretar
from modos import obter_modo


def mostrar_resultado(resultado):
    print()
    print("-" * 60)
    print("                    LEITURA")
    print("-" * 60)

    print(f"Modo    : {resultado['modo']}")
    print(f"Pergunta: {resultado['pergunta']}")
    print()

    for simbolo in resultado["simbolos"]:
        print(f"[ {simbolo['posicao']} ]")
        print(f"Símbolo  : {simbolo['nome']}")
        print(f"Categoria: {simbolo['categoria']}")
        print(f"Leitura  : {simbolo['significado']}")
        print()

    leitura_final = interpretar(resultado["simbolos"])

    print("=" * 60)
    print("                 INTERPRETAÇÃO")
    print("=" * 60)
    print()
    print(leitura_final)
    print()
    print("=" * 60)


def executar_modo(modo):
    nome = modo["nome"]

    print()
    print(f"        {nome}")
    print(f"        {modo['descricao']}")
    print()

    if nome == "MENSAGEM DO MOMENTO":
        pergunta = "Qual é a mensagem simbólica deste momento?"

    else:
        pergunta = input("Digite a sua pergunta: ").strip()

        if not pergunta:
            print("\nNenhuma pergunta foi fornecida.")
            return

    resultado = consultar(pergunta, nome)
    mostrar_resultado(resultado)


def iniciar():
    print()
    print("=" * 60)
    print("                    OLHO DE DEUS")
    print("=" * 60)
    print("NÚCLEO: ONLINE")
    print("SISTEMA: OPERACIONAL")
    print()

    while True:
        historico = obter_historico()
        print(f"CONSULTAS REGISTRADAS: {len(historico)}")

        modo = obter_modo()

        if modo is None:
            print()
            print("OLHO DE DEUS encerrado.")
            break

        executar_modo(modo)


if __name__ == "__main__":
    iniciar()
