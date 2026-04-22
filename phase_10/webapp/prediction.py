from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PIPELINE_PATH = BASE_DIR / "models" / "rain_tomorrow_pipeline.joblib"
METRICS_PATH = BASE_DIR / "models" / "training_metrics.json"

_bundle: dict[str, Any] | None = None


def pipeline_available() -> bool:
    return PIPELINE_PATH.is_file()


def load_bundle() -> dict[str, Any] | None:
    global _bundle
    if _bundle is None and pipeline_available():
        _bundle = joblib.load(PIPELINE_PATH)
    return _bundle


def read_training_metrics() -> dict[str, Any] | None:
    if not METRICS_PATH.is_file():
        return None
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def predict_rain_tomorrow(form_values: dict[str, str]) -> dict[str, Any]:
    bundle = load_bundle()
    if bundle is None:
        raise FileNotFoundError("Trained model not found. Run train_rain_model.py first.")

    pipeline = bundle["pipeline"]
    columns: list[str] = bundle["feature_columns"]

    row: dict[str, Any] = {c: None for c in columns}

    float_fields = {
        "MinTemp",
        "MaxTemp",
        "Rainfall",
        "Evaporation",
        "Sunshine",
        "WindGustSpeed",
        "WindSpeed9am",
        "WindSpeed3pm",
        "Humidity9am",
        "Humidity3pm",
        "Pressure9am",
        "Pressure3pm",
        "Cloud9am",
        "Cloud3pm",
        "Temp9am",
        "Temp3pm",
    }
    string_fields = {
        "Location",
        "WindGustDir",
        "WindDir9am",
        "WindDir3pm",
        "RainToday",
    }

    for key in float_fields:
        if key in form_values and str(form_values[key]).strip() != "":
            try:
                row[key] = float(form_values[key])
            except ValueError:
                row[key] = None

    for key in string_fields:
        if key in form_values and str(form_values[key]).strip() != "":
            row[key] = str(form_values[key]).strip()

    frame = pd.DataFrame([row], columns=columns)

    proba = pipeline.predict_proba(frame)[0]
    label = int(pipeline.predict(frame)[0])
    rain_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

    return {
        "label": label,
        "rain_probability": rain_prob,
        "prediction_text": "Rain likely tomorrow" if label == 1 else "Rain unlikely tomorrow",
    }
