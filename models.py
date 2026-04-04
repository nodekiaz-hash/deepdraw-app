from pydantic import BaseModel


class CalculationRequest(BaseModel):
    d: float
    h: float
    f: float
    k: float


class CalculationResponse(BaseModel):
    D0: float
    Dreal: float
    draw_ratio: float