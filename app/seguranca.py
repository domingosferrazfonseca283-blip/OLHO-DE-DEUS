from pathlib import Path


EXTENSOES_NAO_EXECUTAR = {
    ".exe",
    ".bat",
    ".cmd",
    ".sh",
    ".ps1",
    ".com",
    ".msi"
}


def caminho_seguro(caminho):
    try:
        return Path(caminho).expanduser().resolve()
    except (OSError, RuntimeError):
        return None


def pode_ler(caminho):
    caminho = caminho_seguro(caminho)

    if caminho is None:
        return False

    return caminho.exists() and caminho.is_file()


def pode_analisar(caminho):
    caminho = caminho_seguro(caminho)

    if caminho is None:
        return False

    return caminho.exists()


def eh_executavel(caminho):
    caminho = caminho_seguro(caminho)

    if caminho is None:
        return False

    return caminho.suffix.lower() in EXTENSOES_NAO_EXECUTAR


def status_seguranca():
    return {
        "somente_leitura": True,
        "executar_arquivos": False,
        "apagar_arquivos": False,
        "modificar_arquivos": False,
        "internet_obrigatoria": False
    }
