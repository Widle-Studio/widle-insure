import os
import joblib
import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MLFraudDetectionService:
    def __init__(self):
        self.model = None

        # Try to load the trained model
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "scripts", "models", "fraud_isolation_forest.joblib")

            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Loaded ML Fraud Detection Model.")
            else:
                logger.warning("ML Fraud Model not found. Will fallback to basic heuristics.")
        except Exception as e:
            logger.error(f"Failed to load ML Fraud Model: {e}")

    def analyze_fraud_risk(self, estimated_cost: float, days_since_incident: int, claim_history_count: int) -> Dict[str, Any]:
        """
        Analyze fraud risk using the trained Isolation Forest anomaly detection model.
        Returns a dict with 'is_anomaly' (bool) and 'risk_score' (0-100).
        """
        if not self.model:
            # Fallback heuristic
            score = 0
            if estimated_cost > 10000: score += 15
            if days_since_incident > 30: score += 20
            if claim_history_count > 1: score += 25

            return {
                "is_anomaly": score > 40,
                "risk_score": min(score, 100),
                "method": "heuristic"
            }

        try:
            # Predict using the model
            df = pd.DataFrame([{
                "estimated_cost": estimated_cost,
                "days_since_incident": days_since_incident,
                "claim_history_count": claim_history_count
            }])

            # Output is 1 for normal, -1 for anomaly
            prediction = self.model.predict(df)[0]

            # Decision function gives a continuous anomaly score (lower is more anomalous)
            anomaly_score_raw = self.model.decision_function(df)[0]

            # Normalize score to 0-100 risk score (heuristic normalization)
            # If anomaly_score_raw is ~0, risk is ~50. If deeply negative, risk approaches 100.
            risk_score = max(0, min(100, int(50 - (anomaly_score_raw * 100))))

            return {
                "is_anomaly": bool(prediction == -1),
                "risk_score": risk_score,
                "method": "ml_isolation_forest"
            }

        except Exception as e:
            logger.error(f"ML Fraud Prediction error: {e}")
            return {
                "is_anomaly": False,
                "risk_score": 0,
                "method": "error_fallback"
            }

fraud_detection_service = MLFraudDetectionService()
