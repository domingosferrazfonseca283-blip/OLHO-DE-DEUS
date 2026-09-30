from pathlib import Path
from collections import Counter
from datetime import datetime


def analisar_pasta(caminho):
    pasta = Path(caminho).expanduser().resolve()

    if not pasta.exists():
        return {
            "erro": "A pasta não existe.",
            "caminho": str(pasta)
        }

    if not pasta.is_dir():
        return {
            "erro": "O caminho informado não é uma pasta.",
            "caminho": str(pasta)
        }

    total_arquivos = 0
    total_pastas = 0
    tamanho_total = 0
    extensoes = Counter()

    arquivo_maior = None
    maior_tamanho = 0

    for item in pasta.rglob("*"):

        try:
            if item.is_dir():
                total_pastas += 1
                continue

            if not item.is_file():
                continue

            total_arquivos += 1

            tamanho = item.stat().st_size
            tamanho_total += tamanho

            extensao = item.suffix.lower()

            if extensao:
                extensoes[extensao] += 1
            else:
                extensoes["[sem extensão]"] += 1

            if tamanho > maior_tamanho:
                maior_tamanho = tamanho
                arquivo_maior = str(item)

        except (PermissionError, OSError):
            continue

    return {
        "caminho": str(pasta),
        "total_arquivos": total_arquivos,
        "total_pastas": total_pastas,
        "tamanho_total": tamanho_total,
        "extensoes": dict(extensoes),
        "arquivo_maior": arquivo_maior,
        "maior_tamanho": maior_tamanho,
        "data": datetime.now().isoformat(
            timespec="seconds"
        )
    }


def formatar_tamanho(bytes_valor):
    unidades = ["B", "KB", "MB", "GB", "TB"]

    tamanho = float(bytes_valor)

    for unidade in unidades:
        if tamanho < 1024:
            return f"{tamanho:.2f} {unidade}"

        tamanho /= 1024

    return f"{tamanho:.2f} PB"


def gerar_relatorio(caminho):
    resultado = analisar_pasta(caminho)

    if "erro" in resultado:
        return (
            "══════════════════════════════════════\n"
            "          SCANNER LOCAL\n"
            "══════════════════════════════════════\n\n"
            f"ERRO: {resultado['erro']}\n"
            f"CAMINHO: {resultado['caminho']}\n"
        )

    linhas = [
        "══════════════════════════════════════",
        "          SCANNER LOCAL",
        "══════════════════════════════════════",
        "",
        f"CAMINHO: {resultado['caminho']}",
        "",
        f"ARQUIVOS: {resultado['total_arquivos']}",
        f"PASTAS:   {resultado['total_pastas']}",
        f"TAMANHO:  {formatar_tamanho(resultado['tamanho_total'])}",
        "",
        "EXTENSÕES:",
    ]

    for extensao, quantidade in sorted(
        resultado["extensoes"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        linhas.append(
            f"  {extensao}: {quantidade}"
        )

    linhas.extend([
        "",
        "MAIOR ARQUIVO:",
        f"  {resultado['arquivo_maior']}",
        f"  {formatar_tamanho(resultado['maior_tamanho'])}",
        "",
        "──────────────────────────────────────",
        "FONTE: SISTEMA DE ARQUIVOS LOCAL",
        "REDE: NÃO UTILIZADA",
        "STATUS: DADOS REAIS",
        "──────────────────────────────────────"
    ])

    return "\n".join(linhas)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Uso:\n"
            "python app/scanner.py /caminho/da/pasta"
        )
        raise SystemExit(1)

    print(
        gerar_relatorio(sys.argv[1])
    )
