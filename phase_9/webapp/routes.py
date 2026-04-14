from flask import Blueprint, render_template, request

from .database import get_session
from .models import QueryHistory
from .services import (
    build_dashboard_metrics,
    ensure_plot_assets,
    get_dataset,
    list_locations,
    run_query,
)

web = Blueprint("web", __name__)


@web.get("/")
def index():
    df = get_dataset()
    metrics = build_dashboard_metrics(df)
    return render_template("index.html", metrics=metrics)


@web.route("/query", methods=["GET", "POST"])
def query():
    df = get_dataset()
    locations = list_locations(df)

    selected_location = ""
    min_max_temp = ""
    rainy_only = False
    results = None
    result_count = 0

    if request.method == "POST":
        selected_location = request.form.get("location", "").strip()
        min_temp_raw = request.form.get("min_max_temp", "").strip()
        rainy_only = request.form.get("rainy_only") == "on"

        min_temp_value = None
        if min_temp_raw:
            try:
                min_temp_value = float(min_temp_raw)
                min_max_temp = min_temp_raw
            except ValueError:
                min_temp_value = None
                min_max_temp = ""

        results_df = run_query(
            df=df,
            location=selected_location or None,
            min_max_temp=min_temp_value,
            rainy_only=rainy_only,
        )
        result_count = len(results_df)
        results = results_df.head(25).to_dict(orient="records")

        session = get_session()
        try:
            session.add(
                QueryHistory(
                    location=selected_location or "All",
                    min_max_temp=min_temp_value or 0.0,
                    rainy_only=str(rainy_only).lower(),
                    result_count=result_count,
                )
            )
            session.commit()
        finally:
            session.close()

    return render_template(
        "query.html",
        locations=locations,
        selected_location=selected_location,
        min_max_temp=min_max_temp,
        rainy_only=rainy_only,
        results=results,
        result_count=result_count,
    )


@web.get("/visualizations")
def visualizations():
    df = get_dataset()
    files = ensure_plot_assets(df)
    return render_template("visualizations.html", files=files)


@web.get("/history")
def history():
    session = get_session()
    try:
        entries = (
            session.query(QueryHistory)
            .order_by(QueryHistory.created_at.desc())
            .limit(50)
            .all()
        )
    finally:
        session.close()
    return render_template("history.html", entries=entries)


@web.get("/health")
def health():
    return {"status": "ok"}
