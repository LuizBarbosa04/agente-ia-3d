
from ollama import Client
from pydantic import ValidationError

from executar_cad import executar_cad
from gerenciador_projetos import criar_diretorio_projeto
from models import CaixaInterpretacao, CaixaParametros


MODELO = "qwen3:4b"

client = Client(
    host="http://127.0.0.1:11434",
    timeout=90
)

PERGUNTAS = {
    "comprimento": "Qual será o comprimento da caixa, em mm? ",
    "largura": "Qual será a largura da caixa, em mm? ",
    "altura": "Qual será a altura da caixa, em mm? ",
    "espessura": "Qual será a espessura das paredes, em mm? "
}


def perguntar_sim_nao(pergunta: str) -> bool:
    while True:
        resposta = input(pergunta).strip().lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "não", "nao"):
            return False

        print("Resposta inválida. Digite s ou n.")


def interpretar_pedido(pedido: str) -> CaixaInterpretacao:
    resposta = client.chat(
        model=MODELO,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extraia parâmetros geométricos para impressão 3D. "
                    "Utilize milímetros e trabalhe somente com caixas. "
                    "Comprimento, largura e altura são dimensões EXTERNAS. "
                    "Nunca subtraia a espessura dessas medidas. "
                    "Não invente informações ausentes. "
                    "Use null para qualquer campo não informado. "
                    "Não faça cálculos geométricos. "
                    "Retorne somente o JSON conforme o esquema."
                )
            },
            {
                "role": "user",
                "content": pedido
            }
        ],
        format=CaixaInterpretacao.model_json_schema(),
        think=False,
        options={"temperature": 0}
    )

    return CaixaInterpretacao.model_validate_json(
        resposta.message.content
    )


def completar_parametros(interpretacao: CaixaInterpretacao) -> dict:
    dados = interpretacao.model_dump()

    for campo, pergunta in PERGUNTAS.items():
        if dados[campo] is None:
            while True:
                resposta = input(pergunta).strip().replace(",", ".")

                try:
                    valor = float(resposta)

                    if not 0 < valor <= (
                        250 if campo == "altura" else 220
                    ):
                        print(
                            "Informe uma medida positiva dentro do limite."
                        )
                        continue

                    dados[campo] = valor
                    break

                except ValueError:
                    print("Digite um número válido.")

    if dados["fundo_fechado"] is None:
        dados["fundo_fechado"] = perguntar_sim_nao(
            "A caixa terá fundo fechado? (s/n): "
        )

    if dados["tampa"] is None:
        dados["tampa"] = perguntar_sim_nao(
            "A caixa terá tampa? (s/n): "
        )

    return dados


def main():
    pedido = input("Descreva a peça que deseja criar: ").strip()

    if not pedido:
        print("Nenhuma solicitação informada.")
        return

    try:
        interpretacao = interpretar_pedido(pedido)
        dados = completar_parametros(interpretacao)
        parametros = CaixaParametros.model_validate(dados)

        if not parametros.fundo_fechado:
            raise ValueError(
                "Caixas com fundo aberto ainda não são suportadas."
            )

        if parametros.tampa:
            raise ValueError(
                "Caixas com tampa ainda não são suportadas."
            )

    except (ValidationError, ValueError) as erro:
        print(f"Solicitação rejeitada: {erro}")
        return

    except Exception as erro:
        print(f"Falha no processamento: {erro}")
        return

    print("\nParâmetros interpretados e validados:")
    print(parametros.model_dump_json(indent=2))

    confirmacao = perguntar_sim_nao(
        "\nConfirma essas dimensões? (s/n): "
    )

    if not confirmacao:
        print("Operação cancelada.")
        return

    try:
        caminho_projeto = criar_diretorio_projeto(parametros.tipo)

        conteudo_json = parametros.model_dump_json(indent=2)

        (caminho_projeto / "parametros.json").write_text(
            conteudo_json,
            encoding="utf-8"
        )

        print(f"\nProjeto criado em: {caminho_projeto}")
        print("Iniciando geração do modelo 3D...")

        executar_cad(caminho_projeto)

    except (OSError, RuntimeError, ValueError) as erro:
        print(f"Falha na geração CAD: {erro}")
        return

    print("\nModelo 3D gerado com sucesso!")
    print(f"Arquivos disponíveis em: {caminho_projeto}")


if __name__ == "__main__":
    main()
