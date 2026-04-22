"""Train and persist a scikit-learn pipeline for RainTomorrow."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "data" / "Weather Training Data.csv"
MODEL_DIR = BASE_DIR / "models"
PIPELINE_PATH = MODEL_DIR / "rain_tomorrow_pipeline.joblib"
METRICS_PATH = MODEL_DIR / "training_metrics.json"


def _prepare_target(series: pd.Series) -> pd.Series:
    if series.dtype == object or str(series.dtype) == "string":
        mapped = series.astype(str).str.strip().str.lower()
        return mapped.map({"yes": 1, "no": 0, "true": 1, "false": 0}).fillna(0).astype(int)
    return series.fillna(0).astype(int)


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    if "RainTomorrow" not in df.columns:
        raise ValueError("CSV must contain a RainTomorrow column.")

    if "row ID" in df.columns:
        df = df.drop(columns=["row ID"])

    y = _prepare_target(df["RainTomorrow"])
    X = df.drop(columns=["RainTomorrow"])

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=True),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "clf",
                LogisticRegression(
                    max_iter=500,
                    class_weight="balanced",
                    solver="liblinear",
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": model,
            "feature_columns": list(X.columns),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
        },
        PIPELINE_PATH,
    )

    METRICS_PATH.write_text(
        json.dumps(
            {
                "holdout_accuracy": acc,
                "n_train": int(len(X_train)),
                "n_test": int(len(X_test)),
                "target": "RainTomorrow",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved pipeline to {PIPELINE_PATH}")
    print(f"Holdout accuracy: {acc:.4f}")
    print(f"Metrics written to {METRICS_PATH}")


if __name__ == "__main__":
    main()
