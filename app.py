import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained pipeline
model = joblib.load("fraud_model.pkl")


@app.route("/")
def home():
    return jsonify({
        "message": "Credit Card Fraud Detection API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Send transaction details as JSON"}), 400

        required_fields = [
            "TransactionAmount",
            "TransactionFrequency",
            "AverageTransactionAmount",
            "InternationalTransaction",
            "TransactionHour"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        X = pd.DataFrame([{
            field: data[field] for field in required_fields
        }])

        prediction = int(model.predict(X)[0])
        classes = list(model.classes_)
        probabilities = model.predict_proba(X)[0]
        risk = probabilities[classes.index(1)] * 100

        return jsonify({
            "prediction": prediction,
            "result": "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction",
            "fraud_probability": round(float(risk), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
