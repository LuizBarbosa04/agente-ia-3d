
import os
import subprocess
from pathlib import Path

from gerenciador_status import registrar_status


DIRETORIO_BASE = Path(__file__).resolve().parent

FREECAD = Path(
    r"C:\Users\Luiz Gustavo\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe"
)

SCRIPT_CAD = DIRETORIO_BASE / "cad" / "gerar_caixa.py"


def executar_cad(caminho_projeto: Path) -> tuple[Path, Path]:
    registrar_status(
        caminho_projeto,
        "processando",
        "Iniciando geração do modelo CAD."
    )

    try:
        if not FREECAD.is_file():
            raise FileNotFoundError(
                "Executável do FreeCAD não encontrado."
            )

        if not SCRIPT_CAD.is_file():
            raise FileNotFoundError(
                "Script de geração CAD não encontrado."
            )

        if not caminho_projeto.is_dir():
            raise FileNotFoundError(
                "Diretório do projeto não encontrado."
            )

        arquivo_fcstd = caminho_projeto / "modelo.FCStd"
        arquivo_stl = caminho_projeto / "modelo.stl"

        if arquivo_fcstd.exists() or arquivo_stl.exists():
            raise FileExistsError(
                "O projeto já possui arquivos CAD."
            )

        ambiente = os.environ.copy()
        ambiente["AGENTE_3D_OUTPUT"] = str(
            caminho_projeto.resolve()
        )

        resultado = subprocess.run(
            [str(FREECAD), str(SCRIPT_CAD)],
            cwd=caminho_projeto,
            env=ambiente,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=120,
            check=False
        )

        if resultado.stdout:
            print(resultado.stdout)

        if resultado.stderr:
            print(resultado.stderr)

        if resultado.returncode != 0:
            raise RuntimeError(
                f"FreeCAD retornou código {resultado.returncode}."
            )

        for arquivo in (arquivo_fcstd, arquivo_stl):
            if not arquivo.is_file() or arquivo.stat().st_size == 0:
                raise RuntimeError(
                    f"Arquivo CAD ausente ou vazio: {arquivo.name}"
                )

        registrar_status(
            caminho_projeto,
            "concluido",
            "Modelo CAD gerado e verificado com sucesso."
        )

        print("Automação CAD concluída.")
        print("Arquivos verificados com sucesso.")

        return arquivo_fcstd, arquivo_stl

    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as erro:
        registrar_status(
            caminho_projeto,
            "falhou",
            str(erro)
        )

        raise
