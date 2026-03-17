"""
Main Entry Point (Phase 7)

Async data loading and multiprocessing for stats and plot generation.
Same results as sequential version, improved efficiency.

Author: Brady S
Course: Python Development - Spring 2026
"""

import asyncio
import logging
import os
from multiprocessing import Pool

from aussie_weather import DataFetcher, DataProcessor, DataStorage, DataVisualizer
from aussie_weather.stats import compute_stats_string
from aussie_weather.visualizer import generate_plot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PLOTS_DIR = "phase_7/plots"
SUMMARY_PATH = "phase_7/weather_summary.txt"

PLOT_TASKS = [
    ("temp_distribution", "phase_7/plots/temp_distribution.png"),
    ("rainfall_by_location", "phase_7/plots/rainfall_by_location.png"),
    ("temp_trends", "phase_7/plots/temp_trends.png"),
    ("correlation_heatmap", "phase_7/plots/correlation_heatmap.png"),
    ("rainy_vs_dry_days", "phase_7/plots/rainy_vs_dry.png"),
]


async def load_data_async():
    fetcher = DataFetcher("data/Weather Training Data.csv")
    await fetcher.load_async()
    return fetcher


def run_parallel_stats_and_plots(df):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    plot_args = [(name, df, path) for name, path in PLOT_TASKS]
    with Pool(6) as pool:
        stats_result = pool.apply_async(compute_stats_string, (df,))
        plot_results = pool.map(generate_plot, plot_args)
        stats_string = stats_result.get()
    return stats_string, plot_results


def main():
    logger.info("Starting weather data analysis (async load + multiprocessing)")
    try:
        fetcher = asyncio.run(load_data_async())
        df = fetcher.data
        logger.info(f"Loaded {fetcher.record_count} records from CSV")

        print(f"Loaded data: {fetcher}")
        print(f"Columns: {fetcher.columns}\n")

        processor = DataProcessor(df)
        logger.info("DataProcessor initialized")
        print(f"Processor: {processor}\n")

        stats_string, _ = run_parallel_stats_and_plots(df)
        print(stats_string)
        logger.info("Statistics and plots computed in parallel")

        storage = DataStorage(df, SUMMARY_PATH)
        output_file = storage.write_summary()
        logger.info(f"Summary written to {output_file}")
        print(f"Summary written to {output_file}")

        print("\n" + "=" * 50)
        print("DATA VISUALIZATION")
        print("=" * 50 + "\n")

        visualizer = DataVisualizer(df)
        print("--- Functional Programming Examples ---\n")

        rainy_days = visualizer.filter_rainy_days()
        print(f"Rainy days: {len(rainy_days)} records")

        hot_days = visualizer.filter_hot_days(threshold=35)
        print(f"Hot days >35°C: {len(hot_days)} records")

        temps_f = visualizer.map_temp_to_fahrenheit('MaxTemp')
        print(f"Converted {len(temps_f)} temperatures to Fahrenheit")
        print(f"  Sample: {temps_f[0]:.1f}°F, {temps_f[1]:.1f}°F, {temps_f[2]:.1f}°F...")

        total_rain = visualizer.reduce_total_rainfall()
        print(f"Total rainfall: {total_rain:.2f}mm")

        avg_temp = visualizer.reduce_average_temp('MaxTemp')
        print(f"Average MaxTemp: {avg_temp:.2f}°C")

        print("\n--- Top 5 Locations by Rainfall ---")
        rainfall_by_loc = visualizer.get_rainfall_by_location().head(5)
        for loc, rain in rainfall_by_loc.items():
            print(f"  {loc}: {rain:.2f}mm")

        print("\n--- Plots generated (via multiprocessing) ---")
        for _, path in PLOT_TASKS:
            print(f"  {path}")
        print("\nAll visualizations complete!")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: {e}")
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        print(f"Data Error: {e}")
    except IOError as e:
        logger.error(f"I/O error: {e}")
        print(f"File Error: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
