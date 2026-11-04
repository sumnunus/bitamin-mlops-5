# Week 4 — FastAPI 모델 서빙 (hoofitech 개인 실습)

`week3`에서 저장한 `churn_model.joblib`(sklearn Pipeline)을 FastAPI로 서빙한다.

```bash
cd week4/hoofitech
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload
```

| 파일 | 역할 |
| --- | --- |
| `main.py` (hoofitech 실습 버전) | 앱, 서버 시작 시 모델 1회 로드(`lifespan`), `GET /`, `POST /predict` |
| `schema.py` | 고객 정보 입력용 Pydantic 스키마 `CustomerInput` (+ Swagger 예시값) |
| `../churn_model.joblib` | 전처리 + 모델이 함께 저장된 Pipeline (week4 공용) |

## API 명세

`POST /predict` — 입력(19개 필드, `schema.py` 참고) → 출력

```json
{"churn": 1, "churn_probability": 0.851}
```

형식이 틀린 입력은 모델에 닿기 전에 `422`로 차단된다.

## 체크포인트

### 1. FastAPI 서버 기동 및 Swagger 접속
`http://127.0.0.1:8000/docs`

![cp1](images/cp1-docs.png)

### 2. Pydantic 스키마 정의
`schema.py`의 `CustomerInput`이 Swagger Schemas에 표시된다.

![cp2](images/cp2-schema.png)

### 3. 모델 로드 및 `/predict` 구현
코드는 `main.py` 참고. `lifespan`에서 서버 시작 시 `churn_model.joblib`을 1번만 로드한다.

![cp3](images/cp3-startup-log.png)

### 4. Swagger에서 예측 요청 성공
POST `/predict` → Try it out → Execute → 200

![cp4](images/cp4-swagger-predict.png)

### 5. Postman으로 동일 요청 테스트
같은 고객 데이터로 POST → `200 OK`, Swagger와 같은 확률

![cp5](images/cp5-postman.png)

`{"churn": 1, "churn_probability": 0.85102503974859}`

형식이 틀린 입력(예: `{"tenure":"abc"}`)은 `422`로 차단된다.

> 이 폴더는 `lifespan` 방식으로 모델을 로드한 개인 실습 버전이다. 팀 공용 코드는 상위 `week4/`의 `main.py`·`schema.py`. 모델 파일은 `week4/churn_model.joblib`을 같이 쓴다.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH)  # 서버 시작 시 1번만 로드
    logger.info(f"model loaded: {MODEL_PATH.name} ({type(model).__name__})")
    yield

app = FastAPI(title="Telco Churn Prediction API", lifespan=lifespan)
```
