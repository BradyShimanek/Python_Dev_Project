from pathlib import Path
from typing import Any

import pandas as pd

from aussie_weather.loader import DataFetcher
from aussie_weather.visualizer import DataVisualizer


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR.parent / "data" / "Weather Training Data.csv"
PLOTS_DIR = BASE_DIR / "static" / "plots"

_dataset_cache: pd.DataFrame | None = None


def get_dataset() -> pd.DataFrame:
    global _dataset_cache
    if _dataset_cache is None:
        fetcher = DataFetcher(str(CSV_PATH))
        fetcher.load()
        _dataset_cache = fetcher.data
    return _dataset_cache


def build_dashboard_metrics(df: pd.DataFrame) -> dict[str, Any]:
    visualizer = DataVisualizer(df)
    rainfall_by_loc = visualizer.get_rainfall_by_location().head(5)
    return {
        "record_count": len(df),
        "column_count": len(df.columns),
        "average_max_temp": round(visualizer.reduce_average_temp("MaxTemp"), 2),
        "total_rainfall": round(visualizer.reduce_total_rainfall(), 2),
        "top_locations": [(name, round(value, 2)) for name, value in rainfall_by_loc.items()],
    }


def run_query(
    df: pd.DataFrame,
    location: str | None,
    min_max_temp: float | None,
    rainy_only: bool,
) -> pd.DataFrame:
    result = df.copy()

    if location:
        result = result[result["Location"] == location]
    if min_max_temp is not None:
        result = result[result["MaxTemp"] >= min_max_temp]
    if rainy_only:
        result = result[result["Rainfall"] > 0]

    return result


def list_locations(df: pd.DataFrame) -> list[str]:
    return sorted(df["Location"].dropna().unique().tolist())


def ensure_plot_assets(df: pd.DataFrame) -> list[str]:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    visualizer = DataVisualizer(df)
    plots = [
        ("temp_distribution.png", visualizer.plot_temp_distribution),
        ("rainfall_by_location.png", visualizer.plot_rainfall_by_location),
        ("temp_trends.png", visualizer.plot_temp_trends),
        ("correlation_heatmap.png", visualizer.plot_correlation_heatmap),
        ("rainy_vs_dry.png", visualizer.plot_rainy_vs_dry_days),
    ]
    output_files: list[str] = []

    for filename, func in plots:
        path = str(PLOTS_DIR / filename)
        func(save_path=path, show=False)
        output_files.append(filename)

    return output_files
