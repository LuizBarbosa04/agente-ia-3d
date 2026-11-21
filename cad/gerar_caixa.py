
import json
import math
import os
from pathlib import Path

import FreeCAD
import Part
import Mesh


destino = os.environ.get("AGENTE_3D_OUTPUT")

if not destino:
    raise RuntimeError("Diretório de saída não informado.")

saida = Path(destino).resolve()

if not saida.is_dir():
    raise FileNotFoundError("Diretório de saída não encontrado.")

caminho_json = saida / "parametros.json"

if not caminho_json.is_file():
    raise FileNotFoundError(
        "Arquivo de parâmetros do projeto não encontrado."
    )

arquivo_fcstd = saida / "modelo.FCStd"
arquivo_stl = saida / "modelo.stl"

if arquivo_fcstd.exists() or arquivo_stl.exists():
    raise FileExistsError(
        "O diretório já contém arquivos CAD."
    )

with caminho_json.open("r", encoding="utf-8") as arquivo:
    parametros = json.load(arquivo)

if not isinstance(parametros, dict):
    raise ValueError("Os parâmetros devem formar um objeto JSON.")

if parametros.get("tipo") != "caixa":
    raise ValueError("O tipo de modelo não é suportado.")

if parametros.get("fundo_fechado") is not True:
    raise ValueError("Apenas caixas com fundo fechado são suportadas.")

if parametros.get("tampa") is not False:
    raise ValueError("Caixas com tampa ainda não são suportadas.")

limites = {
    "comprimento": 220,
    "largura": 220,
    "altura": 250
}

for campo in ("comprimento", "largura", "altura", "espessura"):
    valor = parametros.get(campo)

    if (
        isinstance(valor, bool)
        or not isinstance(valor, (int, float))
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError(f"Parâmetro inválido: {campo}")

    if campo in limites and valor > limites[campo]:
        raise ValueError(f"{campo} excede o limite configurado.")

comprimento = parametros["comprimento"]
largura = parametros["largura"]
altura = parametros["altura"]
espessura = parametros["espessura"]

if espessura * 2 >= min(comprimento, largura):
    raise ValueError("As paredes impedem a criação da cavidade.")

if espessura >= altura:
    raise ValueError("O fundo não pode ocupar toda a altura.")

externo = Part.makeBox(comprimento, largura, altura)

interno = Part.makeBox(
    comprimento - 2 * espessura,
    largura - 2 * espessura,
    altura - espessura,
    FreeCAD.Vector(espessura, espessura, espessura)
)

geometria = externo.cut(interno)

if geometria.isNull() or not geometria.isValid():
    raise ValueError("A geometria gerada é inválida.")

if len(geometria.Solids) != 1:
    raise ValueError("A geometria não possui exatamente um sólido.")

documento = FreeCAD.newDocument("CaixaJSON")

try:
    objeto = documento.addObject("PartDesign::Feature", "Caixa")
    objeto.Shape = geometria

    documento.recompute()

    documento.saveAs(str(arquivo_fcstd))

    Mesh.export(
        [objeto],
        str(arquivo_stl)
    )

    print("Modelo gerado com sucesso.")
    print(f"Dimensões: {comprimento} x {largura} x {altura} mm")
    print(f"Espessura: {espessura} mm")
    print(f"Volume: {geometria.Volume:.2f} mm³")
    print(f"Arquivos salvos em: {saida}")

finally:
    FreeCAD.closeDocument(documento.Name)
