"""
Main Entry Point

Demonstrates the usage of the aussie_weather package including
data visualization and functional programming features.

Author: Brady S
Course: Python Development - Spring 2026

NOTE: AI was used to assist in the creation of the documentation for this project.
"""

import logging
from aussie_weather import DataFetcher, DataProcessor, DataStorage, DataVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the weather data analysis and visualization."""
    
    logger.info("Starting weather data analysis")
    
    try:
        fetcher = DataFetcher("data/Weather Training Data.csv")
        fetcher.load()
        logger.info(f"Loaded {fetcher.record_count} records from CSV")
        
        print(f"Loaded data: {fetcher}")
        print(f"Columns: {fetcher.columns}\n")
        
        processor = DataProcessor(fetcher.data)
        logger.info("DataProcessor initialized")
        print(f"Processor: {processor}")
        
        processor.print_stats()
        logger.info("Statistics calculated and printed")
        
        storage = DataStorage(fetcher.data, "phase_6/weather_summary.txt")
        output_file = storage.write_summary()
        logger.info(f"Summary written to {output_file}")
        print(f"\nSummary written to {output_file}")
        
        print("\n" + "="*50)
        print("DATA VISUALIZATION")
        print("="*50 + "\n")
        
        visualizer = DataVisualizer(fetcher.data)
        logger.info("DataVisualizer initialized")
        
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
        
        print("\n--- Generating Visualizations ---\n")
        print("1. Temperature Distribution Histogram")
        visualizer.plot_temp_distribution(save_path="phase_6/plots/temp_distribution.png")
        
        print("2. Rainfall by Location Bar Chart")
        visualizer.plot_rainfall_by_location(save_path="phase_6/plots/rainfall_by_location.png")
        
        print("3. Temperature Trends Line Chart")
        visualizer.plot_temp_trends(save_path="phase_6/plots/temp_trends.png")
        
        print("4. Correlation Heatmap")
        visualizer.plot_correlation_heatmap(save_path="phase_6/plots/correlation_heatmap.png")
        
        print("5. Rainy vs Dry Days Pie Chart")
        visualizer.plot_rainy_vs_dry_days(save_path="phase_6/plots/rainy_vs_dry.png")
        
        logger.info("All visualizations generated successfully")
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
