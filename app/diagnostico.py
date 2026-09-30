import os
import platform
import socket
from datetime import datetime


def coletar_diagnostico():
    dados = {
        "sistema": platform.system(),
        "versao": platform.version(),
        "arquitetura": platform.machine(),
        "processador": platform.processor(),
        "hostname": socket.gethostname(),
        "usuario": os.getenv("USER") or os.getenv("USERNAME") or "desconhecido",
        "python": platform.python_version(),
        "data_hora": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    return dados


def formatar_diagnostico():
    dados = coletar_diagnostico()

    linhas = [
        "══════════════════════════════════════",
        "          DIAGNÓSTICO DO SISTEMA",
        "══════════════════════════════════════",
        "",
        f"SISTEMA       : {dados['sistema']}",
        f"VERSÃO        : {dados['versao']}",
        f"ARQUITETURA   : {dados['arquitetura']}",
        f"PROCESSADOR   : {dados['processador']}",
        f"HOSTNAME      : {dados['hostname']}",
        f"USUÁRIO       : {dados['usuario']}",
        f"PYTHON        : {dados['python']}",
        f"DATA/HORA     : {dados['data_hora']}",
        "",
        "FONTE: SISTEMA LOCAL",
        "STATUS: DADOS REAIS",
        ""
    ]

    return "\n".join(linhas)
