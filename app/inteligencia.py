import re
from datetime import datetime

from painel_sistema import obter_dados_sistema
from rede import verificar_rede
from oraculo import obter_historico
from scanner import analisar_pasta, formatar_tamanho
from seguranca import status_seguranca
from web import consultar_web


PALAVRAS_LOCAL = {
    "computador", "sistema", "windows", "processador", "cpu",
    "disco", "armazenamento", "arquivo", "arquivos", "pasta",
    "pastas", "memória", "memoria", "hostname", "usuário",
    "usuario", "python", "local"
}

PALAVRAS_WEB = {
    "hoje", "atual", "agora", "notícia", "noticias",
    "tempo", "clima", "preço", "preco", "cotação",
    "cotacao", "internet", "web", "online", "pesquise",
    "pesquisar", "quem", "onde", "quando", "quanto"
}

PALAVRAS_HISTORICO = {
    "histórico", "historico", "consulta", "consultas",
    "anterior", "anteriores"
}

PALAVRAS_SEGURANCA = {
    "segurança", "seguranca", "proteção", "protecao",
    "somente leitura", "somente leitura"
}


def normalizar(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def eh_comando_scanner(texto):
    texto = normalizar(texto)
    return (
        texto == "scan"
        or texto.startswith("scan ")
        or texto.startswith("scanner ")
        or texto.startswith("analisar pasta ")
        or texto.startswith("analise pasta ")
    )


def extrair_caminho_scanner(texto):
    texto = str(texto).strip()

    prefixos = [
        "analisar pasta ",
        "analise pasta ",
        "scanner ",
        "scan "
    ]

    texto_normalizado = texto.lower()

    for prefixo in prefixos:
        if texto_normalizado.startswith(prefixo):
            caminho = texto[len(prefixo):].strip()
            return caminho.strip('"').strip("'")

    return ""


def classificar_pergunta(pergunta):
    texto = normalizar(pergunta)

    if eh_comando_scanner(texto):
        return "SCANNER"

    if any(palavra in texto for palavra in PALAVRAS_SEGURANCA):
        return "SEGURANÇA"

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

    if any(
        expressao in texto
        for expressao in indicadores_web
    ):
        web = True

    if historico and not local and not web:
        return "HISTÓRICO"

    if local and web:
        return "HÍBRIDO"

    if local:
        return "LOCAL"

    return "WEB"


def resumo_sistema():
    return {
        "fonte": "SISTEMA LOCAL",
        "tipo": "LOCAL",
        "dados": obter_dados_sistema()
    }


def resumo_rede():
    return {
        "fonte": "REDE LOCAL",
        "tipo": "LOCAL",
        "dados": verificar_rede()
    }


def resumo_historico():
    return {
        "fonte": "HISTÓRICO LOCAL",
        "tipo": "HISTÓRICO",
        "dados": obter_historico()
    }


def resumo_seguranca():
    return {
        "fonte": "NÚCLEO DE SEGURANÇA",
        "tipo": "SEGURANÇA",
        "dados": status_seguranca()
    }


def resumo_scanner(caminho):
    dados = analisar_pasta(caminho)

    return {
        "fonte": "SCANNER LOCAL",
        "tipo": "SCANNER",
        "dados": dados
    }


def executar(pergunta):
    pergunta = str(pergunta).strip()

    if not pergunta:
        return {
            "status": "ERRO",
            "mensagem": "Nenhuma pergunta foi fornecida."
        }

    modo = classificar_pergunta(pergunta)

    fontes = []

    if modo == "SCANNER":
        caminho = extrair_caminho_scanner(pergunta)

        if not caminho:
            return {
                "status": "ERRO",
                "modo": modo,
                "pergunta": pergunta,
                "fontes": [],
                "mensagem": (
                    "Informe o caminho da pasta. "
                    "Exemplo: scan C:\\Users"
                )
            }

        fontes.append(
            resumo_scanner(caminho)
        )

    elif modo == "SEGURANÇA":
        fontes.append(
            resumo_seguranca()
        )

    else:
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

    for fonte in resultado.get("fontes", []):
        linhas.extend([
            "──────────────────────────────────────────",
            f"FONTE: {fonte['fonte']}",
            f"TIPO : {fonte['tipo']}",
            ""
        ])

        dados = fonte["dados"]
        tipo = fonte["tipo"]

        if tipo == "LOCAL":
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

        elif tipo == "SEGURANÇA":
            for chave, valor in dados.items():
                linhas.append(
                    f"{chave.upper():22}: {valor}"
                )
            linhas.append("")

        elif tipo == "SCANNER":
            if "erro" in dados:
                linhas.extend([
                    f"ERRO    : {dados['erro']}",
                    f"CAMINHO : {dados['caminho']}",
                    ""
                ])
            else:
                linhas.extend([
                    f"CAMINHO       : {dados['caminho']}",
                    f"ARQUIVOS      : {dados['total_arquivos']}",
                    f"PASTAS        : {dados['total_pastas']}",
                    f"TAMANHO TOTAL : {formatar_tamanho(dados['tamanho_total'])}",
                    "",
                    "EXTENSÕES:"
                ])

                for extensao, quantidade in sorted(
                    dados["extensoes"].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    linhas.append(
                        f"  {extensao}: {quantidade}"
                    )

                linhas.extend([
                    "",
                    f"MAIOR ARQUIVO : {dados['arquivo_maior']}",
                    f"TAMANHO       : {formatar_tamanho(dados['maior_tamanho'])}",
                    ""
                ])

        elif tipo == "HISTÓRICO":
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

        elif tipo == "WEB":
            for numero, item in enumerate(
                dados.get("resultados", []),
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
