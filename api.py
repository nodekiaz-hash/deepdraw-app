from fastapi import FastAPI
from pydantic import BaseModel
from app import process_calculation

app = FastAPI()


class CalculationRequest(BaseModel):
    email: str
    d: float
    h: float
    f: float
    k: float


@app.get("/")
def root():
    return {"message": "DeepDraw API running"}


@app.post("/calculate")
def calculate(request: CalculationRequest):
    result = process_calculation(
        request.email,
        request.d,
        request.h,
        request.f,
        request.k
    )

    # hiba kezelés
    if isinstance(result, str):
        return {
            "status": "error",
            "message": result
        }

    return {
        "status": "success",
        "data": result
    }