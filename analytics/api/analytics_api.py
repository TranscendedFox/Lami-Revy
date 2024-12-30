from fastapi import APIRouter
from service.user_service import get_user_by_id
from analytics.model.prediction_response import PredictionResponse
import pandas as pd
import joblib
import json

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={401: {"analytics": "Not authorized"}}
)


model = joblib.load("analytics/linear_regression_model.joblib")
with open("analytics/model_metrics.json", "r") as metrics_json:
    metrics = json.load(metrics_json)


@router.get("/{user_id}", response_model=PredictionResponse)
async def predict_spending_score(user_id: int):
    user = await get_user_by_id(user_id)

    if user:
        encoded_gender = encode_gender(user.gender)
        input_data = pd.DataFrame({
            'Gender': [encoded_gender],
            'Age': [user.age],
            'Annual Income ($)': [user.annual_income]
        })

        prediction = model.predict(input_data)

        return PredictionResponse(spending_score=prediction[0],
                                  mae= metrics.get("mae", "N/A"),
                                  r2_score= metrics.get("r2_score", "N/A"))


def encode_gender(gender: str) -> int:
    if gender.lower() == "male":
        return 0
    elif gender.lower() == "female":
        return 1
