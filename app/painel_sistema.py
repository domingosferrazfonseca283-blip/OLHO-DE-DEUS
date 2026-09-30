import os
import platform
import shutil
import socket
from datetime import datetime


def obter_dados_sistema():
    try:
        total, usado, livre = shutil.disk_usage("/")

        disco_total_gb = round(total / (1024 ** 3), 2)
        disco_usado_gb = round(usado / (1024 ** 3), 2)
        disco_livre_gb = round(livre / (1024 ** 3), 2)

    except OSError:
        disco_total_gb = 0
        disco_usado_gb = 0
        disco_livre_gb = 0

    return {
        "sistema": platform.system(),
        "versao": platform.version(),
        "release": platform.release(),
        "arquitetura": platform.machine(),
        "processador": platform.processor() or "Não identificado",
        "hostname": socket.gethostname(),
        "usuario": (
            os.getenv("USERNAME")
            or os.getenv("USER")
            or "Não identificado"
        ),
        "python": platform.python_version(),
        "disco_total_gb": disco_total_gb,
        "disco_usado_gb": disco_usado_gb,
        "disco_livre_gb": disco_livre_gb,
        "data_hora": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def gerar_painel():
    dados = obter_dados_sistema()

    return (
        "══════════════════════════════════════════\n"
        "             OLHO DE DEUS\n"
        "          DIAGNÓSTICO LOCAL\n"
        "══════════════════════════════════════════\n\n"

        f"SISTEMA       : {dados['sistema']}\n"
        f"RELEASE       : {dados['release']}\n"
        f"VERSÃO        : {dados['versao']}\n"
        f"ARQUITETURA   : {dados['arquitetura']}\n"
        f"PROCESSADOR   : {dados['processador']}\n"
        f"HOSTNAME      : {dados['hostname']}\n"
        f"USUÁRIO       : {dados['usuario']}\n"
        f"PYTHON        : {dados['python']}\n\n"

        f"DISCO TOTAL   : {dados['disco_total_gb']} GB\n"
        f"DISCO USADO   : {dados['disco_usado_gb']} GB\n"
        f"DISCO LIVRE   : {dados['disco_livre_gb']} GB\n\n"

        f"DATA/HORA     : {dados['data_hora']}\n\n"

        "──────────────────────────────────────────\n"
        "FONTE         : COMPUTADOR LOCAL\n"
        "INTERNET      : NÃO NECESSÁRIA\n"
        "STATUS        : DADOS REAIS\n"
        "──────────────────────────────────────────\n"
    )


if __name__ == "__main__":
    print(gerar_painel())
