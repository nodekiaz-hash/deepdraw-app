from fastapi import FastAPI
from pydantic import BaseModel

from app import process_calculation

app = FastAPI()


# -------------------------
# 📦 REQUEST MODEL
# -------------------------
class CalculationRequest(BaseModel):
    email: str
    d: float
    h: float
    f: float
    k: float
    lang: str = "en"


# -------------------------
# 🚀 ENDPOINT
# -------------------------
@app.post("/calculate")
def calculate(data: CalculationRequest):
    try:
        result = process_calculation(
            email=data.email,
            d=data.d,
            h=data.h,
            f=data.f,
            k=data.k,
            lang=data.lang
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        print("API ERROR:", e)
        return {
            "status": "error",
            "message": str(e)
        }


# -------------------------
# ❤️ HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"status": "API running"}


# -------------------------
# 🚀 START SERVER
# -------------------------
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("api:app", host="0.0.0.0", port=port)