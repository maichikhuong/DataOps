import warnings
warnings.filterwarnings('ignore')
import json
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
# import Schema
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
# import prediction
from ml_flow.predict import model, MODEL_VERSION, prediction_output
app = FastAPI()


@app.get("/")
def home():
    return {'message': 'Insurance Premium Prediction API'}


@app.get("/health")
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_reload': model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = prediction_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
