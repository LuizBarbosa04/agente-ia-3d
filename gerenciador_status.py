
import json
from datetime import datetime
from pathlib import Path


STATUS_VALIDOS = {
    "processando",
    "concluido",
    "falhou"
}


def registrar_status(
    caminho_projeto: Path,
    status: str,
    mensagem: str
) -> None:
    if status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido: {status}")

    if not caminho_projeto.is_dir():
        raise FileNotFoundError(
            "Diretório do projeto não encontrado."
        )

    dados = {
        "status": status,
        "mensagem": mensagem,
        "atualizado_em": datetime.now().astimezone().isoformat(
            timespec="seconds"
        )
    }

    caminho_status = caminho_projeto / "status.json"
    caminho_temporario = caminho_projeto / "status.json.tmp"

    try:
        caminho_temporario.write_text(
            json.dumps(
                dados,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        caminho_temporario.replace(caminho_status)

    finally:
        caminho_temporario.unlink(missing_ok=True)
