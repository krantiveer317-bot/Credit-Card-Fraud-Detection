const API_URL = "http://127.0.0.1:5001";

async function checkApi() {
  const status = document.getElementById("apiStatus");
  try {
    const response = await fetch(`${API_URL}/`);
    if (!response.ok) throw new Error("API unavailable");
    status.textContent = "Connected";
  } catch (error) {
    status.textContent = "Not connected";
  }
}
checkApi();

document.getElementById("predictionForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = document.getElementById("submitBtn");
  button.disabled = true;
  button.textContent = "Analyzing...";

  const payload = {
    TransactionAmount: Number(document.getElementById("TransactionAmount").value),
    TransactionFrequency: Number(document.getElementById("TransactionFrequency").value),
    AverageTransactionAmount: Number(document.getElementById("AverageTransactionAmount").value),
    InternationalTransaction: Number(document.getElementById("InternationalTransaction").value),
    TransactionHour: Number(document.getElementById("TransactionHour").value)
  };

  if (payload.TransactionHour < 0 || payload.TransactionHour > 23) {
    alert("Transaction Hour must be between 0 and 23.");
    button.disabled = false;
    button.innerHTML = 'Analyze transaction <span>→</span>';
    return;
  }

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Prediction failed");

    document.getElementById("resultPlaceholder").classList.add("hidden");
    document.getElementById("resultContent").classList.remove("hidden");

    const fraud = result.prediction === 1;
    const status = document.getElementById("resultStatus");
    status.className = fraud ? "result-status fraud" : "result-status";
    document.getElementById("resultIcon").textContent = fraud ? "!" : "✓";
    document.getElementById("resultText").textContent = result.result;
    document.getElementById("probabilityText").textContent = `${result.fraud_probability}%`;

    const bar = document.getElementById("probabilityBar");
    bar.style.width = `${Math.max(0, Math.min(100, result.fraud_probability))}%`;
    bar.className = fraud ? "progress-fill fraud" : "progress-fill";
    document.getElementById("resultNote").textContent = fraud
      ? "The model flagged this transaction as potentially fraudulent. Review it carefully."
      : "The model classified this transaction as legitimate. This is an estimate, not a guarantee.";
  } catch (error) {
    alert(`Could not get prediction: ${error.message}\nMake sure app.py is running and the model has been trained.`);
  } finally {
    button.disabled = false;
    button.innerHTML = 'Analyze transaction <span>→</span>';
  }
});
