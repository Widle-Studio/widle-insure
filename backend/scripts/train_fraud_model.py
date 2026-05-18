import os

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


def train_fraud_model():
    """
    Train a basic Anomaly Detection model (Isolation Forest)
    using mock dataset of claims for advanced ML fraud detection.
    """
    print("Training ML Fraud Detection Model (Isolation Forest)...")

    # Mock training dataset representing historical claims
    # Columns: [estimated_cost, days_since_incident, claim_history_count]
    data = {
        "estimated_cost": [500, 1500, 2000, 300, 8000, 15000, 450, 1200, 21000, 750, 600, 3500],
        "days_since_incident": [2, 5, 1, 10, 45, 60, 3, 2, 90, 4, 1, 15],
        "claim_history_count": [0, 1, 0, 0, 3, 4, 0, 0, 5, 1, 0, 2]
    }

    df = pd.DataFrame(data)

    # Initialize Isolation Forest
    # contamination=0.15 means we expect ~15% of historical claims to be anomalies/fraud
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(df)

    # Save the trained model
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "models")
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "fraud_isolation_forest.joblib")
    joblib.dump(model, model_path)

    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_fraud_model()
