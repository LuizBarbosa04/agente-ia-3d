
from datetime import datetime
from pathlib import Path


DIRETORIO = Path(__file__).resolve().parent
SAIDA = DIRETORIO / "outputs"


def criar_diretorio_projeto(tipo: str) -> Path:
    if tipo != "caixa":
        raise ValueError("Tipo de projeto não suportado.")

    SAIDA.mkdir(parents=True, exist_ok=True)

    data = datetime.now().strftime("%Y%m%d")

    versao = 1

    while True:
        nome = f"{tipo}_{data}_{versao:03d}"
        caminho = SAIDA / nome

        try:
            caminho.mkdir(exist_ok=False)
            return caminho

        except FileExistsError:
            versao += 1
