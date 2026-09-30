REGRAS = {
    ("ciclo", "incerteza", "direção"):
        "Um ciclo parece estar a chegar a uma fase de transição. "
        "O presente ainda contém elementos pouco claros, mas existe "
        "uma direção possível quando houver maior clareza sobre aquilo "
        "que precisa de ser encerrado.",

    ("visão", "mudança", "direção"):
        "A leitura aponta para atenção, transformação e procura de direção. "
        "Observar primeiro pode ser mais importante do que agir imediatamente.",

    ("estrutura", "incerteza", "direção"):
        "Existe uma estrutura que merece ser observada com cuidado. "
        "A falta de clareza no presente não significa ausência de caminho, "
        "mas recomenda compreender melhor a situação antes de decidir.",

    ("incerteza", "visão", "mudança"):
        "Aquilo que inicialmente parece indefinido pode revelar uma mudança "
        "quando observado por outro ângulo."
}


def interpretar(simbolos):
    categorias = tuple(
        simbolo["categoria"]
        for simbolo in simbolos
    )

    if categorias in REGRAS:
        return REGRAS[categorias]

    return (
        "Os três símbolos formam uma leitura aberta: existe uma relação "
        "entre aquilo que já aconteceu, o estado atual e uma possível "
        "direção futura. A interpretação deve ser usada como reflexão "
        "simbólica, não como previsão factual."
    )
