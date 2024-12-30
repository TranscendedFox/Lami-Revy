from pydantic import BaseModel


class PredictionResponse(BaseModel):
    spending_score: float
    mae: float
    r2_score: float
