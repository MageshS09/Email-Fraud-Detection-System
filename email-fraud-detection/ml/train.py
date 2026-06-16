from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from joblib import dump

DATA_FILE = Path(__file__).resolve().parent / "data.csv"
MODEL_FILE = Path(__file__).resolve().parent / "models" / "email_fraud_model.joblib"


def load_dataset() -> pd.DataFrame:
    if not DATA_FILE.exists():
        records = [
            {"text": "Urgent: Verify your account login", "label": 1},
            {"text": "Your invoice is attached", "label": 1},
            {"text": "Meeting agenda for tomorrow", "label": 0},
            {"text": "Quarterly report available", "label": 0},
            {"text": "Important: wire transfer update", "label": 1},
        ]
        return pd.DataFrame(records)
    return pd.read_csv(DATA_FILE)


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("vectorizer", TfidfVectorizer(max_features=2000, stop_words="english")),
        ("classifier", GradientBoostingClassifier(n_estimators=100, random_state=42)),
    ])


def train() -> None:
    df = load_dataset()
    X = df["text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    dump(pipeline, MODEL_FILE)
    print(f"Trained model saved to {MODEL_FILE}")


if __name__ == "__main__":
    train()
