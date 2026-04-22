# Australian Weather Web App — Phase 10

Extends the three-tier Flask application with **predictive modeling** using **scikit-learn**: a pipeline trained on the weather dataset predicts whether it will **rain tomorrow** (`RainTomorrow`).

## Architecture

- **UI tier:** Jinja templates, HTML, CSS; `/predict` form for model inputs
- **Business tier:** Flask routes; `webapp/prediction.py` loads the saved pipeline and returns class probability
- **Data tier:** SQLite (`QueryHistory`) unchanged from the previous phase

## Model

- **Algorithm:** `LogisticRegression` (balanced class weights) inside a `Pipeline` with:
  - Median imputation + scaling for numeric columns
  - Most-frequent imputation + one-hot encoding for categorical columns
- **Target:** `RainTomorrow` (binary)
- **Training script:** `train_rain_model.py` reads `data/Weather Training Data.csv`, fits the pipeline, writes:
  - `models/rain_tomorrow_pipeline.joblib` — serialized pipeline and column metadata
  - `models/training_metrics.json` — holdout accuracy and row counts

Train once before using `/predict` (or after updating the dataset):

```bash
source venv/bin/activate
pip install -r phase_10/requirements.txt
python phase_10/train_rain_model.py
```

## Run the application

From the repository root:

```bash
source venv/bin/activate
pip install -r phase_10/requirements.txt
python phase_10/main.py
```

If you work only inside `phase_10/`, use `pip install -r requirements.txt` and `python main.py`.

Open in the browser:

- `http://127.0.0.1:5001/`

Port **5001** avoids conflicts with macOS AirPlay on port 5000. To use 5000 instead, disable AirPlay Receiver under **System Settings → General → AirDrop & Handoff**, then change the port in `main.py`.

## Routes

| Path | Description |
|------|-------------|
| `/` | Dashboard |
| `/query` | Filtered data query |
| `/visualizations` | Charts |
| `/predict` | Rain-tomorrow prediction form and results |
| `/history` | Query history |
| `/health` | JSON health check |

## Project layout

```
phase_10/
├── main.py
├── train_rain_model.py
├── requirements.txt
├── models/
│   ├── rain_tomorrow_pipeline.joblib   (created by training script)
│   └── training_metrics.json           (created by training script)
├── webapp/
├── templates/
├── static/
└── aussie_weather/
```

## Dependencies

Listed in `requirements.txt` (Flask, SQLAlchemy, pandas, matplotlib, seaborn, scikit-learn, joblib).

## SQLite

Application database file (created at runtime):

- `phase_10/weather_app.db`

Stores `QueryHistory` entries from the query form.
