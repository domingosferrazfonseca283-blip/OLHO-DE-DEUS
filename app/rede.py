import json
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_CONFIG = BASE_DIR / "config" / "config.json"


def carregar_config():
    try:
        with open(
            ARQUIVO_CONFIG,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (OSError, json.JSONDecodeError):
        return {}


def internet_permitida():
    config = carregar_config()
    return bool(config.get("internet", False))


def modo_online_ativado():
    config = carregar_config()
    return bool(config.get("modo_online", False))


def modo_offline_ativado():
    config = carregar_config()
    return bool(config.get("modo_offline", False))


def testar_conexao(timeout=5):
    if not internet_permitida():
        return False

    try:
        urllib.request.urlopen(
            "https://www.google.com/generate_204",
            timeout=timeout
        )
        return True

    except Exception:
        return False


def verificar_rede():
    config = carregar_config()

    obrigatoria = (
        config.get("rede") == "OBRIGATÓRIA"
    )

    conectada = testar_conexao()

    return {
        "internet_permitida": internet_permitida(),
        "modo_online": modo_online_ativado(),
        "modo_offline": modo_offline_ativado(),
        "obrigatoria": obrigatoria,
        "conectada": conectada,
        "status": (
            "ONLINE"
            if conectada
            else "SEM CONEXÃO"
        )
    }


def status_rede():
    dados = verificar_rede()

    return {
        "modo": dados["status"],
        "internet": dados["internet_permitida"],
        "online": dados["modo_online"],
        "obrigatoria": dados["obrigatoria"],
        "conectada": dados["conectada"]
    }


if __name__ == "__main__":
    dados = verificar_rede()

    print()
    print("======================================")
    print("          REDE OLHO DE DEUS")
    print("======================================")
    print()
    print(f"INTERNET PERMITIDA : {dados['internet_permitida']}")
    print(f"MODO ONLINE        : {dados['modo_online']}")
    print(f"MODO OFFLINE       : {dados['modo_offline']}")
    print(f"INTERNET OBRIGATÓRIA: {dados['obrigatoria']}")
    print(f"CONEXÃO            : {dados['conectada']}")
    print(f"STATUS             : {dados['status']}")
    print()
