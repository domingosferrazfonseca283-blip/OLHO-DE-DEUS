import json
import urllib.parse
import urllib.request
from datetime import datetime


USER_AGENT = (
    "OLHO-DE-DEUS/0.4 "
    "(motor de consulta online)"
)


def consultar_web(pergunta, limite=5):

    pergunta = str(pergunta).strip()

    if not pergunta:
        return {
            "status": "ERRO",
            "pergunta": "",
            "resultados": [],
            "mensagem": "Nenhuma consulta foi fornecida."
        }

    consulta = urllib.parse.quote(pergunta)

    url = (
        "https://api.duckduckgo.com/"
        f"?q={consulta}"
        "&format=json"
        "&no_html=1"
        "&skip_disambig=1"
    )

    requisicao = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT
        }
    )

    try:
        with urllib.request.urlopen(
            requisicao,
            timeout=10
        ) as resposta:

            dados = json.loads(
                resposta.read().decode(
                    "utf-8",
                    errors="replace"
                )
            )

    except Exception as erro:

        return {
            "status": "ERRO",
            "pergunta": pergunta,
            "resultados": [],
            "mensagem": f"Falha na consulta online: {erro}"
        }

    resultados = []

    if dados.get("AbstractText"):
        resultados.append({
            "titulo": dados.get(
                "Heading",
                "Resumo"
            ),
            "texto": dados["AbstractText"],
            "url": dados.get(
                "AbstractURL",
                ""
            ),
            "fonte": dados.get(
                "AbstractSource",
                "DuckDuckGo"
            )
        })

    for item in dados.get(
        "RelatedTopics",
        []
    ):

        if not isinstance(item, dict):
            continue

        texto = item.get("Text")
        url_resultado = item.get("FirstURL")

        if not texto:
            continue

        resultados.append({
            "titulo": texto[:100],
            "texto": texto,
            "url": url_resultado or "",
            "fonte": "DuckDuckGo"
        })

        if len(resultados) >= limite:
            break

    return {
        "status": "ONLINE",
        "pergunta": pergunta,
        "resultados": resultados,
        "quantidade": len(resultados),
        "data_hora": datetime.now().isoformat(
            timespec="seconds"
        )
    }


def formatar_resultado(resultado):

    linhas = [
        "╔══════════════════════════════════════════════╗",
        "║             CONSULTA ONLINE                 ║",
        "╚══════════════════════════════════════════════╝",
        "",
        f"CONSULTA: {resultado.get('pergunta', '')}",
        f"STATUS: {resultado.get('status', '')}",
        ""
    ]

    if resultado.get("mensagem"):
        linhas.extend([
            resultado["mensagem"],
            ""
        ])

    resultados = resultado.get(
        "resultados",
        []
    )

    if not resultados:
        linhas.extend([
            "Nenhum resultado encontrado.",
            ""
        ])

    for numero, item in enumerate(
        resultados,
        start=1
    ):

        linhas.extend([
            f"[{numero}] {item.get('titulo', '')}",
            "",
            item.get('texto', ''),
            "",
            f"FONTE: {item.get('fonte', '')}",
            f"URL: {item.get('url', '')}",
            "",
            "──────────────────────────────────────────"
        ])

    linhas.extend([
        "",
        f"RESULTADOS: {len(resultados)}",
        f"DATA/HORA: {resultado.get('data_hora', '')}",
        "",
        "FONTE: INTERNET",
        "MODO: CONSULTA ONLINE",
        "STATUS: DADOS EXTERNOS"
    ])

    return "\n".join(linhas)


if __name__ == "__main__":

    pergunta = input(
        "Digite uma consulta online: "
    ).strip()

    resultado = consultar_web(
        pergunta
    )

    print()
    print(
        formatar_resultado(
            resultado
        )
    )
