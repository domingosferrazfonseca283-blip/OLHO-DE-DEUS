import re
from datetime import datetime

from painel_sistema import obter_dados_sistema
from rede import verificar_rede
from oraculo import obter_historico
from web import consultar_web


PALAVRAS_LOCAL = {
    "computador",
    "sistema",
    "windows",
    "processador",
    "cpu",
    "disco",
    "armazenamento",
    "arquivo",
    "arquivos",
    "pasta",
    "pastas",
    "memória",
    "memoria",
    "hostname",
    "usuário",
    "usuario",
    "python",
    "local"
}

PALAVRAS_WEB = {
    "hoje",
    "atual",
    "agora",
    "notícia",
    "noticias",
    "notícia",
    "tempo",
    "clima",
    "preço",
    "preco",
    "cotação",
    "cotacao",
    "internet",
    "web",
    "online",
    "pesquise",
    "pesquisar",
    "quem",
    "onde",
    "quando",
    "quanto"
}

PALAVRAS_HISTORICO = {
    "histórico",
    "historico",
    "consulta",
    "consultas",
    "anterior",
    "anteriores"
}


def normalizar(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def classificar_pergunta(pergunta):
    texto = normalizar(pergunta)

    local = any(
        palavra in texto
        for palavra in PALAVRAS_LOCAL
    )

    web = any(
        palavra in texto
        for palavra in PALAVRAS_WEB
    )

    historico = any(
        palavra in texto
        for palavra in PALAVRAS_HISTORICO
    )

    indicadores_web = (
        "procure na internet",
        "pesquise na internet",
        "pesquise online",
        "procure online",
        "consulte a internet",
        "consulte a web",
        "informações atuais",
        "informacao atual",
        "informações da internet",
        "dados da internet",
        "na internet",
        "na web",
        "online"
    )

    indicador_expresso_web = any(
        expressao in texto
        for expressao in indicadores_web
    )

    if indicador_expresso_web:
        web = True

    if historico and not local and not web:
        return "HISTÓRICO"

    if local and web:
        return "HÍBRIDO"

    if local:
        return "LOCAL"

    return "WEB"


def resumo_sistema():
    dados = obter_dados_sistema()

    return {
        "fonte": "SISTEMA LOCAL",
        "tipo": "LOCAL",
        "dados": dados
    }


def resumo_rede():
    dados = verificar_rede()

    return {
        "fonte": "REDE LOCAL",
        "tipo": "LOCAL",
        "dados": dados
    }


def resumo_historico():
    historico = obter_historico()

    return {
        "fonte": "HISTÓRICO LOCAL",
        "tipo": "HISTÓRICO",
        "dados": historico
    }


def executar(pergunta):
    pergunta = str(pergunta).strip()

    if not pergunta:
        return {
            "status": "ERRO",
            "mensagem": "Nenhuma pergunta foi fornecida."
        }

    modo = classificar_pergunta(
        pergunta
    )

    fontes = []

    if modo in ("LOCAL", "HÍBRIDO"):

        fontes.append(
            resumo_sistema()
        )

        fontes.append(
            resumo_rede()
        )

    if modo == "HISTÓRICO":

        fontes.append(
            resumo_historico()
        )

    if modo in ("WEB", "HÍBRIDO"):

        rede = verificar_rede()

        if not rede["conectada"]:
            return {
                "status": "SEM CONEXÃO",
                "modo": modo,
                "pergunta": pergunta,
                "fontes": fontes,
                "mensagem": (
                    "A Internet é obrigatória para "
                    "esta consulta e não está disponível."
                )
            }

        resultado_web = consultar_web(
            pergunta
        )

        fontes.append({
            "fonte": "INTERNET",
            "tipo": "WEB",
            "dados": resultado_web
        })

    return {
        "status": "OK",
        "modo": modo,
        "pergunta": pergunta,
        "fontes": fontes,
        "data_hora": datetime.now().isoformat(
            timespec="seconds"
        )
    }


def formatar_resposta(resultado):

    linhas = [
        "╔══════════════════════════════════════════════╗",
        "║           MOTOR DE INTELIGÊNCIA             ║",
        "╚══════════════════════════════════════════════╝",
        "",
        f"PERGUNTA : {resultado.get('pergunta', '')}",
        f"STATUS   : {resultado.get('status', '')}",
        f"MODO     : {resultado.get('modo', '')}",
        ""
    ]

    if resultado.get("mensagem"):
        linhas.extend([
            resultado["mensagem"],
            ""
        ])

    for fonte in resultado.get(
        "fontes",
        []
    ):

        linhas.extend([
            "──────────────────────────────────────────",
            f"FONTE: {fonte['fonte']}",
            f"TIPO : {fonte['tipo']}",
            ""
        ])

        dados = fonte["dados"]

        if fonte["tipo"] == "LOCAL":

            if fonte["fonte"] == "SISTEMA LOCAL":

                linhas.extend([
                    f"SISTEMA     : {dados['sistema']}",
                    f"RELEASE     : {dados['release']}",
                    f"ARQUITETURA : {dados['arquitetura']}",
                    f"HOSTNAME    : {dados['hostname']}",
                    f"DISCO TOTAL : {dados['disco_total_gb']} GB",
                    f"DISCO LIVRE : {dados['disco_livre_gb']} GB",
                    ""
                ])

            else:

                linhas.extend([
                    f"STATUS      : {dados['status']}",
                    f"INTERNET    : {dados['conectada']}",
                    f"MODO ONLINE : {dados['modo_online']}",
                    ""
                ])

        elif fonte["tipo"] == "HISTÓRICO":

            linhas.append(
                f"CONSULTAS REGISTRADAS: {len(dados)}"
            )

            for item in dados[-5:]:
                linhas.extend([
                    "",
                    f"DATA: {item.get('data', '')}",
                    f"MODO: {item.get('modo', '')}",
                    f"PERGUNTA: {item.get('pergunta', '')}"
                ])

        elif fonte["tipo"] == "WEB":

            web = dados

            for numero, item in enumerate(
                web.get("resultados", []),
                start=1
            ):

                linhas.extend([
                    f"[{numero}] {item.get('titulo', '')}",
                    item.get('texto', ''),
                    f"FONTE: {item.get('fonte', '')}",
                    f"URL: {item.get('url', '')}",
                    ""
                ])

    linhas.extend([
        "──────────────────────────────────────────",
        f"DATA/HORA: {resultado.get('data_hora', '')}",
        "",
        "O MOTOR NÃO INVENTA DADOS.",
        "CADA INFORMAÇÃO É IDENTIFICADA PELA SUA FONTE."
    ])

    return "\n".join(linhas)


if __name__ == "__main__":

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║           MOTOR DE INTELIGÊNCIA             ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    pergunta = input(
        "Digite uma pergunta: "
    ).strip()

    resultado = executar(
        pergunta
    )

    print()
    print(
        formatar_resposta(
            resultado
        )
    )
