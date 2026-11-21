
import os
import subprocess
from pathlib import Path


DIRETORIO = Path(__file__).resolve().parent

FREECAD = Path(
    r"C:\Users\Luiz Gustavo\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe"
)

SCRIPT = DIRETORIO / "cad" / "gerar_caixa.py"


def executar_cad(caminho_projeto: Path):
    caminho_projeto = Path(caminho_projeto).resolve()

    if not FREECAD.is_file():
        raise FileNotFoundError("FreeCADCmd não encontrado.")

    if not SCRIPT.is_file():
        raise FileNotFoundError("Script CAD não encontrado.")

    if not caminho_projeto.is_dir():
        raise FileNotFoundError(
            f"Diretório do projeto não encontrado: {caminho_projeto}"
        )

    arquivos = [
        caminho_projeto / "modelo.FCStd",
        caminho_projeto / "modelo.stl"
    ]

    if any(arquivo.exists() for arquivo in arquivos):
        raise FileExistsError(
            "O diretório já contém arquivos CAD. "
            "Utilize um diretório exclusivo para cada geração."
        )

    ambiente = os.environ.copy()
    ambiente["AGENTE_3D_OUTPUT"] = str(caminho_projeto)

    try:
        resultado = subprocess.run(
            [str(FREECAD), str(SCRIPT)],
            cwd=str(DIRETORIO),
            env=ambiente,
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

    return arquivos
