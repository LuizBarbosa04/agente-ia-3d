
from models import CaixaInterpretacao


caixa = CaixaInterpretacao(
    tipo="caixa",
    comprimento=100,
    largura=60,
    altura=None,
    espessura=None,
    fundo_fechado=True,
    tampa=False
)

print("Parâmetros interpretados:")
print(caixa.model_dump_json(indent=2))

campos_ausentes = [
    campo
    for campo in (
        "comprimento",
        "largura",
        "altura",
        "espessura",
        "fundo_fechado",
        "tampa"
    )
    if getattr(caixa, campo) is None
]

print("\nInformações ausentes:")
for campo in campos_ausentes:
    print(f"- {campo}")
