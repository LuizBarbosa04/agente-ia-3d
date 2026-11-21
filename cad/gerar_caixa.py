
import json
import math
from pathlib import Path

import FreeCAD
import Part
import Mesh


diretorio = Path(__file__).resolve().parent.parent
caminho_json = diretorio / "parametros_caixa.json"
saida = diretorio / "outputs"

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

saida.mkdir(parents=True, exist_ok=True)

documento = FreeCAD.newDocument("CaixaJSON")

objeto = documento.addObject("PartDesign::Feature", "Caixa")
objeto.Shape = geometria

documento.recompute()

documento.saveAs(str(saida / "caixa_json.FCStd"))

Mesh.export(
    [objeto],
    str(saida / "caixa_json.stl")
)

print("Modelo gerado com sucesso.")
print(f"Dimensões: {comprimento} x {largura} x {altura} mm")
print(f"Espessura: {espessura} mm")
print(f"Volume: {geometria.Volume:.2f} mm³")
print(f"Arquivos salvos em: {saida}")

FreeCAD.closeDocument(documento.Name)
