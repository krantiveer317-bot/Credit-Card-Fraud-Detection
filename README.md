# Credit Card Fraud Detection — Human-readable feature version

## Project files
- `train.py`: trains a preprocessing + Random Forest pipeline.
- `test.py`: evaluates on the same held-out split used by train.py.
- `app.py`: Flask API with only `GET /` and `POST /predict`.
- `frontend/`: HTML, CSS and JavaScript UI.
- `data/creditcard.csv`: synthetic demo dataset.

## Five model inputs
1. TransactionAmount
2. TransactionFrequency
3. AverageTransactionAmount
4. InternationalTransaction (0 = No, 1 = Yes)
5. TransactionHour (0–23)

## Run (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
python train.py
python test.py
python app.py
```
Keep Flask running. In a second terminal:
```powershell
cd frontend
python -m http.server 5500
```
Open http://localhost:5500

## Important data limitation
The included dataset is synthetic and generated for demonstrating the full workflow with human-readable fields. It is NOT a real bank transaction dataset and its model scores do not establish real-world fraud detection performance. These fields are plausible transaction attributes, but they are simulated. Do not use this model for real payment decisions.
