
import subprocess
from pathlib import Path


DIRETORIO = Path(__file__).resolve().parent

FREECAD = Path(
    r"C:\Users\Luiz Gustavo\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe"
)

SCRIPT = DIRETORIO / "cad" / "gerar_caixa.py"
SAIDA = DIRETORIO / "outputs"


def executar_cad():
    if not FREECAD.is_file():
        raise FileNotFoundError("FreeCADCmd não encontrado.")

    if not SCRIPT.is_file():
        raise FileNotFoundError("Script CAD não encontrado.")

    arquivos = [
        SAIDA / "caixa_json.FCStd",
        SAIDA / "caixa_json.stl"
    ]

    existentes = [arquivo for arquivo in arquivos if arquivo.exists()]

    if existentes:
        versao = 1

        while any(
            (SAIDA / f"caixa_json_v{versao}{arquivo.suffix}").exists()
            for arquivo in arquivos
        ):
            versao += 1

        for arquivo in existentes:
            destino = SAIDA / f"caixa_json_v{versao}{arquivo.suffix}"
            arquivo.rename(destino)
            print(f"Versão anterior preservada: {destino.name}")

    try:
        resultado = subprocess.run(
            [str(FREECAD), str(SCRIPT)],
            cwd=str(DIRETORIO),
            capture_output=True,
            text=True,
            errors="replace",
            timeout=120,
            check=False
        )

    except subprocess.TimeoutExpired as erro:
        raise RuntimeError(
            "O FreeCAD excedeu o tempo limite de 120 segundos."
        ) from erro

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.stderr:
        print(resultado.stderr)

    if resultado.returncode != 0:
        raise RuntimeError(
            f"O FreeCAD terminou com código {resultado.returncode}."
        )

    for arquivo in arquivos:
        if not arquivo.is_file() or arquivo.stat().st_size == 0:
            raise RuntimeError(
                f"Arquivo não gerado corretamente: {arquivo.name}"
            )

    print("Automação CAD concluída.")
    print("Arquivos verificados com sucesso.")


if __name__ == "__main__":
    executar_cad()
