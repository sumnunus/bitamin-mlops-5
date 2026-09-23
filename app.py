import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# 1. 데이터 로드
df = pd.read_csv("WA_FnUseC_TelcoCustomerChurn.csv")


# 2. 학습에 쓰지 않을 컬럼 제거
df = df.drop(columns=["customerID"])


# 3. TotalCharges를 숫자형으로 변환
# 숫자로 변환할 수 없는 공백 값은 NaN으로 처리
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# 4. 입력(X)과 타깃(y) 분리
X = df.drop(columns=["Churn"])
y = df["Churn"]


# 5. 수치형 / 범주형 컬럼 분리
numeric_cols = X.select_dtypes(
    include=["int64", "float64"]
).columns

categorical_cols = X.select_dtypes(
    include=["object"]
).columns


# 수치형 데이터 전처리
# 결측치는 중앙값으로 채우고 스케일링
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# 범주형 데이터 전처리
# 결측치는 최빈값으로 채우고 One-Hot Encoding
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])


# 수치형 / 범주형 전처리를 하나로 결합
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_cols),
    ("cat", categorical_pipeline, categorical_cols)
])


# 6. 학습/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 학습 데이터 기준으로 전처리 학습 및 변환
X_train = preprocessor.fit_transform(X_train)

# 테스트 데이터는 학습된 전처리 규칙으로 변환
X_test = preprocessor.transform(X_test)


# 7. Logistic Regression 모델 학습
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


# 8. Logistic Regression 평가
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Logistic Regression Accuracy: {acc:.4f}")


# 9. Random Forest 모델 학습
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)


# 10. Random Forest 평가 및 기존 모델과 비교
rf_y_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_y_pred)

print(f"Random Forest Accuracy: {rf_acc:.4f}")
print(f"Accuracy Difference (RF - LR): {rf_acc - acc:.4f}")