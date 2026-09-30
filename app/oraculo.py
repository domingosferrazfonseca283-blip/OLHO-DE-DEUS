import json
import random
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

if getattr(sys, "frozen", False):
    DIRETORIO_APLICACAO = Path(sys.executable).resolve().parent
else:
    DIRETORIO_APLICACAO = BASE_DIR

ARQUIVO_SIMBOLOS = BASE_DIR / "data" / "simbolos.json"
ARQUIVO_HISTORICO = DIRETORIO_APLICACAO / "history" / "consultas.json"


def carregar_simbolos():
    with open(
        ARQUIVO_SIMBOLOS,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)


def carregar_historico():
    if not ARQUIVO_HISTORICO.exists():
        return []

    try:
        with open(
            ARQUIVO_HISTORICO,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

        return dados if isinstance(dados, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def guardar_consulta(resultado):
    historico = carregar_historico()

    registro = {
        "data": datetime.now().isoformat(
            timespec="seconds"
        ),
        **resultado
    }

    historico.append(registro)

    ARQUIVO_HISTORICO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivo_temporario = (
        ARQUIVO_HISTORICO.with_suffix(".tmp")
    )

    with open(
        arquivo_temporario,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            historico,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    arquivo_temporario.replace(
        ARQUIVO_HISTORICO
    )


def consultar(
    pergunta,
    modo="LEITURA DE 3 SÍMBOLOS"
):
    simbolos = carregar_simbolos()

    quantidade = min(
        3,
        len(simbolos)
    )

    escolhidos = random.sample(
        simbolos,
        quantidade
    )

    posicoes = [
        "PASSADO",
        "PRESENTE",
        "CAMINHO"
    ]

    simbolos_resultado = []

    for posicao, simbolo in zip(
        posicoes,
        escolhidos
    ):
        simbolos_resultado.append({
            "posicao": posicao,
            "nome": simbolo["nome"],
            "categoria": simbolo["categoria"],
            "significado": simbolo["significado"]
        })

    resultado = {
        "modo": modo,
        "pergunta": pergunta,
        "simbolos": simbolos_resultado
    }

    guardar_consulta(resultado)

    return resultado


def obter_historico():
    return carregar_historico()
