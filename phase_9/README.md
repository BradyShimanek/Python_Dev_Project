# Australian Weather Web App - Phase 9

This phase converts the weather analysis workflow into a 3-tier web application:

- **UI tier:** Browser interface built with Flask + Jinja templates, HTML, and CSS
- **Business tier:** Flask route and service logic for weather queries and analytics
- **Data tier:** SQLite persistence using SQLAlchemy

## Features

- Dashboard with dataset overview (records, columns, average max temp, total rainfall)
- Query interface with filters:
  - Location
  - Minimum `MaxTemp`
  - Rainy-days-only toggle
- Visualization page that renders chart assets from the weather dataset
- Query history page backed by SQLite
- Health endpoint for quick runtime checks

## Technology

- Python
- Flask
- Jinja2
- SQLite
- SQLAlchemy
- pandas
- matplotlib / seaborn

## Project Structure

```
phase_9/
├── main.py
├── requirements.txt
├── weather_app.db
├── webapp/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── query.html
│   ├── visualizations.html
│   └── history.html
├── static/
│   ├── css/styles.css
│   └── plots/
└── aussie_weather/
```

## Run Instructions

Dependencies are listed in `phase_9/requirements.txt` so you can install everything in one step.

From project root:

```bash
source venv/bin/activate
pip install -r phase_9/requirements.txt
python phase_9/main.py
```

If you run from inside `phase_9/` (for example after unzipping only that folder), use `pip install -r requirements.txt` and `python main.py` instead.

Open in browser:

- `http://127.0.0.1:5001/`

The app uses port **5001** because on many Macs **5000** is taken by AirPlay Receiver, which can respond with HTTP 403 to normal browser requests. If you prefer 5000, turn off **AirPlay Receiver** under **System Settings → General → AirDrop & Handoff** (or **Sharing** on older macOS), then change the port in `main.py`.

## Routes

- `/` - dashboard
- `/query` - query form and filtered results
- `/visualizations` - chart gallery
- `/history` - persisted query history
- `/health` - service status response

## Data Persistence

SQLite database file:

- `phase_9/weather_app.db`

Current persisted entity:

- `QueryHistory` with query parameters, result count, and timestamp
