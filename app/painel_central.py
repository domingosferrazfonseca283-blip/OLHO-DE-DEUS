from datetime import datetime

from nucleo import NucleoOlhoDeDeus
from rede import verificar_rede
from painel_sistema import obter_dados_sistema
from seguranca import status_seguranca
from oraculo import obter_historico


class PainelCentral:
    def __init__(self):
        self.nucleo = NucleoOlhoDeDeus()

    def iniciar(self):
        return self.nucleo.iniciar()

    def gerar_estado(self):
        rede = verificar_rede()
        sistema = obter_dados_sistema()
        seguranca = status_seguranca()
        historico = obter_historico()

        return {
            "aplicacao": "OLHO DE DEUS",
            "versao": self.nucleo.config.get(
                "versao",
                "desconhecida"
            ),
            "status": (
                "ONLINE"
                if rede["conectada"]
                else "SEM CONEXÃO"
            ),
            "internet": rede["conectada"],
            "modo_online": rede["modo_online"],
            "modo_offline": rede["modo_offline"],
            "sistema": sistema,
            "seguranca": seguranca,
            "consultas": len(historico),
            "atualizacao": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    def resumo(self):
        estado = self.gerar_estado()
        sistema = estado["sistema"]
        seguranca = estado["seguranca"]

        linhas = [
            "",
            "╔══════════════════════════════════════════════╗",
            "║              ◉ OLHO DE DEUS                 ║",
            "║             PAINEL CENTRAL                  ║",
            "╠══════════════════════════════════════════════╣",
            "",
            f"  STATUS       : {estado['status']}",
            f"  INTERNET     : {estado['internet']}",
            f"  MODO ONLINE  : {estado['modo_online']}",
            f"  VERSÃO       : {estado['versao']}",
            "",
            "  ───────── SISTEMA ─────────",
            "",
            f"  SISTEMA      : {sistema['sistema']}",
            f"  RELEASE      : {sistema['release']}",
            f"  ARQUITETURA  : {sistema['arquitetura']}",
            f"  HOSTNAME     : {sistema['hostname']}",
            f"  DISCO TOTAL  : {sistema['disco_total_gb']} GB",
            f"  DISCO LIVRE  : {sistema['disco_livre_gb']} GB",
            "",
            "  ───────── SEGURANÇA ───────",
            "",
            f"  SOMENTE LEITURA : "
            f"{seguranca['somente_leitura']}",
            f"  EXECUÇÃO        : "
            f"{seguranca['executar_arquivos']}",
            f"  EXCLUSÃO        : "
            f"{seguranca['apagar_arquivos']}",
            f"  MODIFICAÇÃO     : "
            f"{seguranca['modificar_arquivos']}",
            "",
            "  ───────── HISTÓRICO ───────",
            "",
            f"  CONSULTAS       : {estado['consultas']}",
            "",
            f"  ATUALIZAÇÃO     : {estado['atualizacao']}",
            "",
            "╚══════════════════════════════════════════════╝",
            ""
        ]

        return "\n".join(linhas)


if __name__ == "__main__":
    painel = PainelCentral()

    try:
        painel.iniciar()
        print(painel.resumo())

    except ConnectionError as erro:
        print()
        print("==============================================")
        print("       OLHO DE DEUS — BLOQUEADO")
        print("==============================================")
        print()
        print(str(erro))
        print()
