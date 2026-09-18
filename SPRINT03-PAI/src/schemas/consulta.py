from pydantic import BaseModel, Field, field_validator
from typing import Literal

class ConsultaRecargaGoodWe(BaseModel):
    modelo_carregador: Literal["GW7K-HCA-20", "GW11K-HCA-20", "GW22K-HCA-20", "Geral / Desconhecido"] = Field(
        description="Modelo exato do carregador veicular GoodWe identificado na consulta"
    )
    potencia_kw: float = Field(
        description="Potência nominal identificada em kW (ex: 7.0, 11.0, 22.0)"
    )
    suporta_ocpp: bool = Field(
        description="Indica se o dispositivo possui suporte nativo ao protocolo OCPP"
    )
    explicacao_tecnica: str = Field(
        description="Resumo técnico focado nas regras de negócio da linha HCA G2"
    )

    @field_validator("potencia_kw")
    @classmethod
    def validar_potencia_goodwe(cls, valor: float) -> float:
        potencias_validas = [0.0, 7.0, 11.0, 22.0]
        if valor not in potencias_validas:
            raise ValueError("Potência em kW incompatível com as especificações da linha GoodWe HCA G2.")
        return valor