
from ollama import Client

from models import CaixaParametros


client = Client(host="http://127.0.0.1:11434")

response = client.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "system",
            "content": (
                "Você extrai parâmetros geométricos de solicitações "
                "para impressão 3D. Utilize milímetros. "
                "Não invente medidas ausentes. "
                "Retorne somente os parâmetros solicitados."
            )
        },
        {
            "role": "user",
            "content": (
                "Crie uma caixa retangular de 80 x 50 x 30 mm, "
                "com paredes de 2 mm, fundo fechado e sem tampa."
            )
        }
    ],
    format=CaixaParametros.model_json_schema(),
    options={"temperature": 0}
)

try:
    parametros = CaixaParametros.model_validate_json(
        response.message.content
    )

    print("Parâmetros validados:")
    print(parametros.model_dump_json(indent=2))

except ValueError as erro:
    print(f"Erro de validação: {erro}")
