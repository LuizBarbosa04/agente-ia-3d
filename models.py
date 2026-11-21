
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CaixaInterpretacao(BaseModel):
    tipo: Literal["caixa"]
    comprimento: float | None
    largura: float | None
    altura: float | None
    espessura: float | None
    fundo_fechado: bool | None
    tampa: bool | None


class CaixaParametros(BaseModel):
    tipo: Literal["caixa"]
    comprimento: float = Field(gt=0, le=220)
    largura: float = Field(gt=0, le=220)
    altura: float = Field(gt=0, le=250)
    espessura: float = Field(gt=0)
    fundo_fechado: bool
    tampa: bool

    @model_validator(mode="after")
    def validar_geometria(self):
        if self.espessura * 2 >= min(
            self.comprimento,
            self.largura
        ):
            raise ValueError(
                "A espessura das paredes impede a criação "
                "de um espaço interno válido."
            )

        if self.fundo_fechado and self.espessura >= self.altura:
            raise ValueError(
                "A espessura do fundo deve ser menor que a altura."
            )

        return self
