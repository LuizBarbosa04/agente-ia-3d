
from pydantic import ValidationError

from models import CaixaParametros


try:
    caixa = CaixaParametros(
        tipo="caixa",
        comprimento=20,
        largura=15,
        altura=30,
        espessura=10,
        fundo_fechado=True,
        tampa=False
    )

    print("Parâmetros aceitos:")
    print(caixa.model_dump_json(indent=2))

except ValidationError as erro:
    print("Parâmetros rejeitados corretamente:")
    print(erro)
