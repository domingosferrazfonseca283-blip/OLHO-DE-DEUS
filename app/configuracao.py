import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_CONFIG = BASE_DIR / "config" / "config.json"


def carregar_configuracao():
    if not ARQUIVO_CONFIG.exists():
        return {}

    try:
        with open(
            ARQUIVO_CONFIG,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        return {}


def obter_config(chave, padrao=None):
    config = carregar_configuracao()
    return config.get(chave, padrao)
