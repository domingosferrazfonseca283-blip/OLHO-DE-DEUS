from datetime import datetime

from configuracao import carregar_configuracao
from diagnostico import coletar_diagnostico
from painel_sistema import obter_dados_sistema
from rede import verificar_rede
from seguranca import status_seguranca


class NucleoOlhoDeDeus:
    def __init__(self):
        self.config = carregar_configuracao()
        self.inicializado = False

    def iniciar(self):
        self.config = carregar_configuracao()

        rede = verificar_rede()

        if self.config.get("rede") == "OBRIGATÓRIA":
            if not rede["conectada"]:
                raise ConnectionError(
                    "A Internet é obrigatória e não está disponível."
                )

        self.inicializado = True

        return {
            "status": "OPERACIONAL",
            "data_hora": datetime.now().isoformat(
                timespec="seconds"
            ),
            "rede": rede
        }

    def diagnostico(self):
        if not self.inicializado:
            self.iniciar()

        return coletar_diagnostico()

    def sistema(self):
        if not self.inicializado:
            self.iniciar()

        return obter_dados_sistema()

    def seguranca(self):
        return status_seguranca()

    def estado(self):
        rede = verificar_rede()

        return {
            "nome": self.config.get(
                "nome_aplicacao",
                "OLHO DE DEUS"
            ),
            "versao": self.config.get(
                "versao",
                "desconhecida"
            ),
            "modo": self.config.get(
                "modo_inicial",
                "ONLINE"
            ),
            "internet_obrigatoria": (
                self.config.get("rede")
                == "OBRIGATÓRIA"
            ),
            "internet_conectada": rede["conectada"],
            "online": rede["modo_online"],
            "offline": rede["modo_offline"],
            "seguranca": self.seguranca(),
            "inicializado": self.inicializado
        }


def exibir_nucleo():
    nucleo = NucleoOlhoDeDeus()

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║              ◉ OLHO DE DEUS                 ║")
    print("║               NÚCLEO CENTRAL                ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    try:
        resultado = nucleo.iniciar()

    except ConnectionError as erro:
        print("STATUS : BLOQUEADO")
        print(f"MOTIVO : {erro}")
        return

    estado = nucleo.estado()

    print(f"STATUS             : {resultado['status']}")
    print(f"VERSÃO             : {estado['versao']}")
    print(f"MODO                : {estado['modo']}")
    print(
        f"INTERNET OBRIGATÓRIA: "
        f"{estado['internet_obrigatoria']}"
    )
    print(
        f"INTERNET CONECTADA  : "
        f"{estado['internet_conectada']}"
    )
    print(f"MODO ONLINE         : {estado['online']}")
    print(f"MODO OFFLINE        : {estado['offline']}")
    print()
    print("SEGURANÇA")
    print("----------------------------------------------")

    for chave, valor in estado["seguranca"].items():
        print(f"{chave.upper():20}: {valor}")

    print()
    print("NÚCLEO CENTRAL: OPERACIONAL")
    print()


if __name__ == "__main__":
    exibir_nucleo()
