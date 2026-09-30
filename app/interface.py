import tkinter as tk
from tkinter import filedialog, messagebox

from modulos import ModulosOlhoDeDeus


class OlhoDeDeusGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("OLHO DE DEUS")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 620)
        self.root.configure(bg="#05080d")

        self.modulos = ModulosOlhoDeDeus()

        try:
            self.modulos.inicializar()
        except ConnectionError as erro:
            messagebox.showerror(
                "OLHO DE DEUS",
                str(erro)
            )
            root.destroy()
            return

        self.criar_interface()
        self.atualizar_status()

    def criar_interface(self):

        # =========================
        # CABEÇALHO
        # =========================

        topo = tk.Frame(
            self.root,
            bg="#080d14",
            height=70
        )
        topo.pack(
            side="top",
            fill="x"
        )

        titulo = tk.Label(
            topo,
            text="◉  OLHO DE DEUS",
            font=("Segoe UI", 24, "bold"),
            fg="#4de1ff",
            bg="#080d14"
        )
        titulo.pack(
            side="left",
            padx=25,
            pady=15
        )

        self.status_label = tk.Label(
            topo,
            text="● CONECTANDO...",
            font=("Segoe UI", 11, "bold"),
            fg="#4de1ff",
            bg="#080d14"
        )
        self.status_label.pack(
            side="right",
            padx=25
        )

        # =========================
        # MENU LATERAL
        # =========================

        menu = tk.Frame(
            self.root,
            bg="#070b11",
            width=230
        )
        menu.pack(
            side="left",
            fill="y"
        )

        tk.Label(
            menu,
            text="MÓDULOS",
            font=("Segoe UI", 11, "bold"),
            fg="#7f8c9c",
            bg="#070b11"
        ).pack(
            pady=(25, 15)
        )

        botoes = [
            ("◈  COMANDO CENTRAL", self.comando_central),
            ("◈  NÚCLEO", self.mostrar_nucleo),
            ("▣  SISTEMA", self.mostrar_sistema),
            ("⌕  SCANNER", self.escanear),
            ("◎  REDE", self.mostrar_rede),
            ("🌐  WEB", self.consultar_web),
            ("♢  SEGURANÇA", self.mostrar_seguranca),
            ("▤  HISTÓRICO", self.mostrar_historico),
        ]

        for texto, comando in botoes:
            tk.Button(
                menu,
                text=texto,
                command=comando,
                font=("Segoe UI", 10, "bold"),
                fg="#dcecff",
                bg="#0b121c",
                activeforeground="#4de1ff",
                activebackground="#111d2b",
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2"
            ).pack(
                fill="x",
                padx=12,
                pady=3
            )

        # =========================
        # ÁREA CENTRAL
        # =========================

        centro = tk.Frame(
            self.root,
            bg="#05080d"
        )
        centro.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.titulo_painel = tk.Label(
            centro,
            text="NÚCLEO CENTRAL",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#05080d"
        )
        self.titulo_painel.pack(
            pady=(30, 10)
        )

        self.olho = tk.Label(
            centro,
            text="◉",
            font=("Segoe UI", 80, "bold"),
            fg="#4de1ff",
            bg="#05080d"
        )
        self.olho.pack(
            pady=10
        )

        # =========================
        # COMANDO CENTRAL
        # =========================

        comando_frame = tk.Frame(
            centro,
            bg="#05080d"
        )
        comando_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 10)
        )

        self.comando = tk.Entry(
            comando_frame,
            font=("Segoe UI", 12),
            bg="#0b121c",
            fg="#ffffff",
            insertbackground="#4de1ff",
            relief="flat"
        )
        self.comando.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        tk.Button(
            comando_frame,
            text="EXECUTAR",
            command=self.executar_comando,
            font=("Segoe UI", 10, "bold"),
            fg="#05080d",
            bg="#4de1ff",
            activebackground="#4de1ff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(
            side="right",
            padx=(10, 0)
        )

        self.comando.bind(
            "<Return>",
            lambda event: self.executar_comando()
        )

        self.resultado = tk.Text(
            centro,
            bg="#080d14",
            fg="#cfe8ff",
            insertbackground="#4de1ff",
            font=("Consolas", 10),
            relief="flat",
            bd=0,
            wrap="word"
        )
        self.resultado.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30)
        )

        self.mostrar_nucleo()

    # =========================
    # UTILITÁRIOS
    # =========================

    def limpar(self):
        self.resultado.delete(
            "1.0",
            tk.END
        )

    def escrever(self, texto):
        self.limpar()
        self.resultado.insert(
            tk.END,
            texto
        )

    def atualizar_status(self):
        try:
            dados = self.modulos.status()

            if dados["internet"]:
                texto = "● ONLINE"
                cor = "#4de1ff"
            else:
                texto = "● SEM CONEXÃO"
                cor = "#ff5555"

            self.status_label.configure(
                text=texto,
                fg=cor
            )

        except Exception:
            self.status_label.configure(
                text="● ERRO",
                fg="#ff5555"
            )

        self.root.after(
            5000,
            self.atualizar_status
        )

    # =========================
    # COMANDO CENTRAL
    # =========================

    def comando_central(self):

        self.titulo_painel.configure(
            text="COMANDO CENTRAL"
        )

        self.escrever(
            "◉ OLHO DE DEUS — COMANDO CENTRAL\\n"
            "══════════════════════════════════════\\n\\n"
            "Digite uma pergunta ou comando no campo acima.\\n\\n"
            "Exemplos:\\n"
            "• Qual é o sistema deste computador?\\n"
            "• Qual é o estado da Internet agora?\\n"
            "• Pesquise informações atuais sobre Windows.\\n"
            "• Analise o computador e pesquise informações relacionadas.\\n\\n"
            "O motor escolherá automaticamente:\\n"
            "LOCAL / WEB / HÍBRIDO / HISTÓRICO"
        )

        self.comando.focus_set()

    def executar_comando(self):

        pergunta = self.comando.get().strip()

        if not pergunta:
            self.comando.focus_set()
            return

        self.titulo_painel.configure(
            text="PROCESSANDO COMANDO"
        )

        self.escrever(
            "◉ OLHO DE DEUS\\n\\n"
            "ANALISANDO COMANDO...\\n"
            "IDENTIFICANDO FONTES...\\n"
            "CONSULTANDO DADOS...\\n\\n"
            "AGUARDE..."
        )

        self.root.update_idletasks()

        try:

            resultado = self.modulos.inteligencia(
                pergunta
            )

            self.titulo_painel.configure(
                text="RESULTADO DA ANÁLISE"
            )

            self.escrever(
                resultado
            )

        except Exception as erro:

            self.titulo_painel.configure(
                text="ERRO"
            )

            self.escrever(
                "FALHA AO PROCESSAR COMANDO\\n\\n"
                f"{erro}"
            )

    # =========================
    # NÚCLEO
    # =========================

    def mostrar_nucleo(self):

        dados = self.modulos.resumo()

        sistema = dados["sistema"]
        seguranca = dados["seguranca"]

        texto = f"""
╔══════════════════════════════════════════════╗
║              ◉ OLHO DE DEUS                 ║
║              NÚCLEO CENTRAL                 ║
╚══════════════════════════════════════════════╝

STATUS
──────────────────────────────────────────────
REDE              : {dados['status']}
INTERNET          : {dados['internet']}
MODO ONLINE       : {dados['modo_online']}

SISTEMA
──────────────────────────────────────────────
SISTEMA            : {sistema['sistema']}
RELEASE            : {sistema['release']}
ARQUITETURA        : {sistema['arquitetura']}
HOSTNAME           : {sistema['hostname']}
DISCO TOTAL        : {sistema['disco_total_gb']} GB
DISCO LIVRE        : {sistema['disco_livre_gb']} GB

SEGURANÇA
──────────────────────────────────────────────
SOMENTE LEITURA    : {seguranca['somente_leitura']}
EXECUÇÃO           : {seguranca['executar_arquivos']}
EXCLUSÃO           : {seguranca['apagar_arquivos']}
MODIFICAÇÃO        : {seguranca['modificar_arquivos']}

HISTÓRICO
──────────────────────────────────────────────
CONSULTAS          : {dados['consultas']}

ATUALIZAÇÃO
──────────────────────────────────────────────
{dados['horario']}
"""

        self.titulo_painel.configure(
            text="NÚCLEO CENTRAL"
        )

        self.escrever(texto)

    # =========================
    # SISTEMA
    # =========================

    def mostrar_sistema(self):

        dados = self.modulos.sistema()

        texto = f"""
╔══════════════════════════════════════════════╗
║              DIAGNÓSTICO LOCAL              ║
╚══════════════════════════════════════════════╝

SISTEMA       : {dados['sistema']}
RELEASE       : {dados['release']}
VERSÃO        : {dados['versao']}
ARQUITETURA   : {dados['arquitetura']}
PROCESSADOR   : {dados['processador']}
HOSTNAME      : {dados['hostname']}
USUÁRIO       : {dados['usuario']}
PYTHON        : {dados['python']}

ARMAZENAMENTO
──────────────────────────────────────────────
TOTAL         : {dados['disco_total_gb']} GB
USADO         : {dados['disco_usado_gb']} GB
LIVRE         : {dados['disco_livre_gb']} GB

FONTE
──────────────────────────────────────────────
COMPUTADOR LOCAL
DADOS REAIS
"""

        self.titulo_painel.configure(
            text="DIAGNÓSTICO DO SISTEMA"
        )

        self.escrever(texto)

    # =========================
    # SCANNER
    # =========================

    def escanear(self):

        caminho = filedialog.askdirectory(
            title="Escolha uma pasta para analisar"
        )

        if not caminho:
            return

        self.titulo_painel.configure(
            text="SCANNER LOCAL"
        )

        self.escrever(
            "ANALISANDO...\n\n"
            "O scanner é somente leitura.\n"
            "Nenhum arquivo será modificado."
        )

        self.root.update_idletasks()

        try:
            resultado = self.modulos.escanear(
                caminho
            )

            self.escrever(resultado)

        except Exception as erro:
            messagebox.showerror(
                "Scanner",
                str(erro)
            )

    # =========================
    # REDE
    # =========================

    def mostrar_rede(self):

        dados = self.modulos.status()

        texto = f"""
╔══════════════════════════════════════════════╗
║                 REDE                         ║
╚══════════════════════════════════════════════╝

STATUS            : {dados['status']}
INTERNET          : {dados['internet']}
MODO ONLINE       : {dados['modo_online']}
MODO OFFLINE      : {dados['modo_offline']}

A Internet está configurada como
OBRIGATÓRIA para o funcionamento do núcleo.

ÚLTIMA VERIFICAÇÃO
──────────────────────────────────────────────
{dados['horario']}
"""

        self.titulo_painel.configure(
            text="STATUS DA REDE"
        )

        self.escrever(texto)

    # =========================
    # WEB
    # =========================

    def consultar_web(self):

        janela = tk.Toplevel(self.root)
        janela.title("Consulta Online")
        janela.geometry("650x180")
        janela.configure(bg="#070b11")

        tk.Label(
            janela,
            text="CONSULTA ONLINE",
            font=("Segoe UI", 16, "bold"),
            fg="#4de1ff",
            bg="#070b11"
        ).pack(pady=15)

        entrada = tk.Entry(
            janela,
            font=("Segoe UI", 12),
            bg="#0b121c",
            fg="#ffffff",
            insertbackground="#4de1ff",
            relief="flat"
        )
        entrada.pack(
            fill="x",
            padx=30,
            pady=5
        )

        def executar():

            pergunta = entrada.get().strip()

            if not pergunta:
                return

            janela.destroy()

            self.titulo_painel.configure(
                text="CONSULTA ONLINE"
            )

            self.escrever(
                "CONSULTANDO A INTERNET...\\n\\n"
                "Aguarde..."
            )

            self.root.update_idletasks()

            try:
                resultado = self.modulos.web(
                    pergunta
                )

                self.escrever(
                    resultado
                )

            except Exception as erro:
                self.escrever(
                    f"ERRO NA CONSULTA ONLINE\\n\\n{erro}"
                )

        tk.Button(
            janela,
            text="CONSULTAR",
            command=executar,
            font=("Segoe UI", 10, "bold"),
            fg="#05080d",
            bg="#4de1ff",
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2"
        ).pack(pady=15)

        entrada.focus_set()
        janela.bind(
            "<Return>",
            lambda event: executar()
        )

    # =========================
    # SEGURANÇA
    # =========================

    def mostrar_seguranca(self):

        dados = self.modulos.seguranca()

        texto = """
╔══════════════════════════════════════════════╗
║                SEGURANÇA                     ║
╚══════════════════════════════════════════════╝

POLÍTICA ATUAL

SOMENTE LEITURA       : {somente}
EXECUTAR ARQUIVOS     : {executar}
APAGAR ARQUIVOS       : {apagar}
MODIFICAR ARQUIVOS    : {modificar}
INTERNET OBRIGATÓRIA  : {internet}

O scanner e os módulos locais não executam,
apagam ou modificam arquivos.
""".format(
            somente=dados["somente_leitura"],
            executar=dados["executar_arquivos"],
            apagar=dados["apagar_arquivos"],
            modificar=dados["modificar_arquivos"],
            internet=dados["internet_obrigatoria"]
        )

        self.titulo_painel.configure(
            text="CAMADA DE SEGURANÇA"
        )

        self.escrever(texto)

    # =========================
    # HISTÓRICO
    # =========================

    def mostrar_historico(self):

        historico = self.modulos.historico()

        linhas = [
            "╔══════════════════════════════════════════════╗",
            "║                 HISTÓRICO                    ║",
            "╚══════════════════════════════════════════════╝",
            ""
        ]

        if not historico:
            linhas.append(
                "Nenhuma consulta registrada."
            )

        else:
            for numero, item in enumerate(
                reversed(historico),
                start=1
            ):
                linhas.extend([
                    f"[{numero}] {item.get('data', '')}",
                    f"    MODO: {item.get('modo', '')}",
                    f"    PERGUNTA: {item.get('pergunta', '')}",
                    ""
                ])

        self.titulo_painel.configure(
            text="HISTÓRICO"
        )

        self.escrever(
            "\n".join(linhas)
        )


def iniciar_interface():

    root = tk.Tk()

    app = OlhoDeDeusGUI(root)

    root.mainloop()
