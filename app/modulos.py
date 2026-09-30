from datetime import datetime

from nucleo import NucleoOlhoDeDeus
from painel_sistema import obter_dados_sistema
from rede import verificar_rede
from scanner import gerar_relatorio
from seguranca import status_seguranca
from oraculo import obter_historico
from web import consultar_web, formatar_resultado
from inteligencia import executar, formatar_resposta
from web import consultar_web, formatar_resultado
from inteligencia import executar, formatar_resposta


class ModulosOlhoDeDeus:

    def __init__(self):
        self.nucleo = NucleoOlhoDeDeus()

    def inicializar(self):
        return self.nucleo.iniciar()

    def status(self):
        rede = verificar_rede()

        return {
            "status": (
                "ONLINE"
                if rede["conectada"]
                else "SEM CONEXÃO"
            ),
            "internet": rede["conectada"],
            "modo_online": rede["modo_online"],
            "modo_offline": rede["modo_offline"],
            "horario": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    def sistema(self):
        return obter_dados_sistema()

    def seguranca(self):
        return status_seguranca()

    def historico(self):
        return obter_historico()

    def escanear(self, caminho):
        return gerar_relatorio(caminho)

    def web(self, pergunta):
        resultado = consultar_web(pergunta)
        return formatar_resultado(resultado)

    def web(self, pergunta):
        resultado = consultar_web(pergunta)
        return formatar_resultado(resultado)

    def inteligencia(self, pergunta):
        resultado = executar(pergunta)
        return formatar_resposta(resultado)

    def resumo(self):
        rede = self.status()
        sistema = self.sistema()
        seguranca = self.seguranca()
        historico = self.historico()

        return {
            "aplicacao": "OLHO DE DEUS",
            "status": rede["status"],
            "internet": rede["internet"],
            "modo_online": rede["modo_online"],
            "sistema": sistema,
            "seguranca": seguranca,
            "consultas": len(historico),
            "horario": rede["horario"]
        }


if __name__ == "__main__":
    modulo = ModulosOlhoDeDeus()

    try:
        modulo.inicializar()

        dados = modulo.resumo()

        print()
        print("╔══════════════════════════════════════════════╗")
        print("║              ◉ OLHO DE DEUS                 ║")
        print("║              MÓDULOS CENTRAIS               ║")
        print("╚══════════════════════════════════════════════╝")
        print()

        print("STATUS")
        print("----------------------------------------------")
        print(f"REDE          : {dados['status']}")
        print(f"INTERNET      : {dados['internet']}")
        print(f"MODO ONLINE   : {dados['modo_online']}")
        print()

        print("MÓDULOS DISPONÍVEIS")
        print("----------------------------------------------")
        print("1. DIAGNÓSTICO")
        print("2. SISTEMA")
        print("3. SCANNER")
        print("4. REDE")
        print("5. SEGURANÇA")
        print("6. HISTÓRICO")
        print()

        print(
            f"CONSULTAS REGISTRADAS : "
            f"{dados['consultas']}"
        )

        print()
        print("MÓDULOS CENTRAIS: OPERACIONAIS")
        print()

    except ConnectionError as erro:
        print()
        print("OLHO DE DEUS BLOQUEADO")
        print(str(erro))
