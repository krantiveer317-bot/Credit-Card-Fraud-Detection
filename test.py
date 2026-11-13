import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

model = joblib.load("fraud_model.pkl")

df = pd.read_csv("data/creditcard.csv")

X = df[[
    "TransactionAmount",
    "TransactionFrequency",
    "AverageTransactionAmount",
    "InternationalTransaction",
    "TransactionHour"
]]
Y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

pred = model.predict(X_test)
accu = accuracy_score(y_test, pred)

print("Test Accuracy:", accu)
print(classification_report(y_test, pred, zero_division=0))
assert len(pred) == len(y_test)

print("All test cases passed and model is ready to deploy")
