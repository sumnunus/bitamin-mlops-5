import logging
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI

from schema import CustomerInput

logger = logging.getLogger("uvicorn.error")
MODEL_PATH = Path(__file__).parent / "churn_model.joblib"
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH)  # 서버 시작 시 1번만 로드
    logger.info(f"model loaded: {MODEL_PATH.name} ({type(model).__name__})")
    yield


app = FastAPI(title="Telco Churn Prediction API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "ok"}


@app.post("/predict")
def predict(data: CustomerInput):
    X = pd.DataFrame([data.model_dump()])  # 학습 때와 같은 컬럼명으로 1행 DataFrame
    return {
        "churn": int(model.predict(X)[0]),
        "churn_probability": float(model.predict_proba(X)[0][1]),
    }
