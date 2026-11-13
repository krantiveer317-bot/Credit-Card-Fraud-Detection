import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("data/creditcard.csv")

X = df[[
    "TransactionAmount",
    "TransactionFrequency",
    "AverageTransactionAmount",
    "InternationalTransaction",
    "TransactionHour"
]]
y = df["Class"]

numeric = [
    "TransactionAmount",
    "TransactionFrequency",
    "AverageTransactionAmount",
    "InternationalTransaction",
    "TransactionHour"
]

preprocess = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), numeric)
])

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", RandomForestClassifier(
        n_estimators=120,
        random_state=42,
        class_weight="balanced"
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"Test accuracy: {accuracy_score(y_test, pred):.3f}")
print(classification_report(y_test, pred, zero_division=0))

joblib.dump(model, "fraud_model.pkl")
print("Saved model to fraud_model.pkl")
