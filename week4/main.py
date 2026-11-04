import joblib
import pandas as pd
from fastapi import FastAPI

from schema import CustomerInput

app = FastAPI()

# STEP 4: 서버 시작 시 한 번만 로드
model = joblib.load("churn_model.joblib")
print("model loaded:", type(model))


@app.get("/")
def root():
    return {"message": "ok"}


# STEP 5~6: 이탈 예측
@app.post("/predict")
def predict(data: CustomerInput):
    X = pd.DataFrame([data.model_dump()])
    label = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][1])
    return {"churn": label, "churn_probability": proba}
