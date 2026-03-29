"""
Swadhikaar Risk Prediction Model
sklearn-based model trained on health camp screening data.

Predicts:
- Heart risk score (0-100)
- Diabetic risk score (0-100)
- Hypertension risk score (0-100)
- Overall risk category (Low, Moderate, High)
- Overall risk score (0-100)

Features used: systolic_bp, diastolic_bp, heart_rate, respiratory_rate,
oxygen_saturation, blood_glucose, bmi, waist_circumference, perfusion_index,
waist_to_height_ratio, + encoded symptoms and lifestyle factors.
"""

import os
import logging
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional

from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score

logger = logging.getLogger("risk_model")

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "dataset", "PS-3-Use-case-database-1.csv"
)

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")

# Numeric features for regression
NUMERIC_FEATURES = [
    "systolic_bp", "diastolic_bp", "heart_rate", "respiratory_rate",
    "oxygen_saturation", "blood_glucose", "bmi",
    "waist_circumference", "perfusion_index", "waist_to_height_ratio",
]

# Categorical features to encode
CATEGORICAL_FEATURES = [
    "chest_discomfort", "breathlessness", "palpitations",
    "fatigue_weakness", "dizziness_blackouts", "sleep_duration",
    "stress_anxiety", "physical_inactivity", "diet_quality", "family_history",
]

# Target columns
TARGETS_REGRESSION = [
    "heart_risk_total_score",
    "diabetic_risk_total_score",
    "hypertension_risk_total_score",
    "overall_risk_score",
]

TARGET_CLASSIFICATION = "overall_risk_category"


class RiskPredictor:
    """Health risk prediction model using sklearn."""

    def __init__(self):
        self.regressors: dict = {}
        self.classifier: Optional[RandomForestClassifier] = None
        self.label_encoders: dict = {}
        self.category_encoder: Optional[LabelEncoder] = None
        self._trained = False

    def train(self, csv_path: str = CSV_PATH) -> dict:
        """Train the model on health camp CSV data."""
        logger.info(f"Loading data from {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} records")

        # Encode categorical features
        for col in CATEGORICAL_FEATURES:
            le = LabelEncoder()
            df[col] = df[col].fillna("unknown")
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le

        # Fill numeric NaN
        for col in NUMERIC_FEATURES:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

        # Features
        all_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
        X = df[all_features].values

        # Fill target NaN
        for col in TARGETS_REGRESSION:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

        # Train regressors for each risk score
        metrics = {}
        X_train, X_test, _, _ = train_test_split(X, df[TARGETS_REGRESSION[0]], test_size=0.2, random_state=42)

        for target in TARGETS_REGRESSION:
            y = df[target].values
            y_train = y[:len(X_train)]
            y_test = y[len(X_train):]

            model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                random_state=42,
            )
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mae = mean_absolute_error(y_test, predictions)

            self.regressors[target] = model
            metrics[target] = {"mae": round(mae, 2)}
            logger.info(f"  {target}: MAE = {mae:.2f}")

        # Train classifier for overall risk category
        self.category_encoder = LabelEncoder()
        df[TARGET_CLASSIFICATION] = df[TARGET_CLASSIFICATION].fillna("Moderate")
        y_cat = self.category_encoder.fit_transform(df[TARGET_CLASSIFICATION])

        y_cat_train = y_cat[:len(X_train)]
        y_cat_test = y_cat[len(X_train):]

        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42,
        )
        self.classifier.fit(X_train, y_cat_train)
        cat_predictions = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_cat_test, cat_predictions)
        metrics["category_accuracy"] = round(accuracy, 3)
        logger.info(f"  Category accuracy: {accuracy:.3f}")

        self._trained = True
        return metrics

    def predict(self, patient_data: dict) -> dict:
        """
        Predict risk scores for a patient.

        Args:
            patient_data: dict with keys matching NUMERIC_FEATURES + CATEGORICAL_FEATURES

        Returns:
            dict with risk scores and category
        """
        if not self._trained:
            self.train()

        # Build feature vector
        features = []
        for col in NUMERIC_FEATURES:
            val = patient_data.get(col, 0)
            try:
                features.append(float(val) if val is not None else 0.0)
            except (ValueError, TypeError):
                features.append(0.0)

        for col in CATEGORICAL_FEATURES:
            val = str(patient_data.get(col, "unknown")).strip()
            le = self.label_encoders.get(col)
            if le and val in le.classes_:
                features.append(le.transform([val])[0])
            else:
                features.append(0)

        X = np.array([features])

        # Predict risk scores
        result = {}
        for target, model in self.regressors.items():
            score = float(model.predict(X)[0])
            score = max(0, min(100, score))  # Clamp 0-100
            result[target] = round(score, 2)

        # Predict category
        if self.classifier and self.category_encoder:
            cat_idx = self.classifier.predict(X)[0]
            category = self.category_encoder.inverse_transform([cat_idx])[0]
            result["overall_risk_category"] = category
        else:
            # Fallback logic
            overall = result.get("overall_risk_score", 0)
            if overall >= 50:
                result["overall_risk_category"] = "High"
            elif overall >= 30:
                result["overall_risk_category"] = "Moderate"
            else:
                result["overall_risk_category"] = "Low"

        # Add risk levels for each domain
        for domain in ["heart_risk_total_score", "diabetic_risk_total_score", "hypertension_risk_total_score"]:
            score = result.get(domain, 0)
            level_key = domain.replace("_total_score", "_level")
            if score >= 50:
                result[level_key] = "High"
            elif score >= 30:
                result[level_key] = "Moderate"
            else:
                result[level_key] = "Low"

        return result

    def save(self, model_dir: str = MODEL_DIR):
        """Save trained models to disk."""
        os.makedirs(model_dir, exist_ok=True)
        with open(os.path.join(model_dir, "risk_model.pkl"), "wb") as f:
            pickle.dump({
                "regressors": self.regressors,
                "classifier": self.classifier,
                "label_encoders": self.label_encoders,
                "category_encoder": self.category_encoder,
            }, f)
        logger.info(f"Models saved to {model_dir}")

    def load(self, model_dir: str = MODEL_DIR) -> bool:
        """Load trained models from disk."""
        model_path = os.path.join(model_dir, "risk_model.pkl")
        if not os.path.exists(model_path):
            return False
        with open(model_path, "rb") as f:
            data = pickle.load(f)
        self.regressors = data["regressors"]
        self.classifier = data["classifier"]
        self.label_encoders = data["label_encoders"]
        self.category_encoder = data["category_encoder"]
        self._trained = True
        logger.info(f"Models loaded from {model_dir}")
        return True


# Singleton instance
_predictor: Optional[RiskPredictor] = None


def get_predictor() -> RiskPredictor:
    """Get or create the risk predictor singleton."""
    global _predictor
    if _predictor is None:
        _predictor = RiskPredictor()
        if not _predictor.load():
            logger.info("No saved model found, training from CSV...")
            _predictor.train()
            _predictor.save()
    return _predictor


def predict_risk(patient_data: dict) -> dict:
    """Quick risk prediction — returns dict with scores and category."""
    predictor = get_predictor()
    return predictor.predict(patient_data)
