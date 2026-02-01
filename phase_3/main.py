"""
Main Entry Point

Demonstrates the usage of the aussie_weather package.

Author: Brady S
Course: Python Development - Spring 2026

NOTE: AI was used to assist in the creation of the documentation for this project.
"""

from aussie_weather import DataFetcher, DataProcessor, DataStorage


def main():
    """Main function to run the weather data analysis."""
    
    # Create a DataFetcher to load the weather data
    fetcher = DataFetcher("data/Weather Training Data.csv")
    fetcher.load()
    
    print(f"Loaded data: {fetcher}")
    print(f"Columns: {fetcher.columns}\n")
    
    # Create a DataProcessor to analyze the data
    processor = DataProcessor(fetcher.data)
    print(f"Processor: {processor}")
    
    # Print descriptive statistics
    processor.print_stats()
    
    # Create a DataStorage to save the summary
    storage = DataStorage(fetcher.data, "phase_3/weather_summary.txt")
    output_file = storage.write_summary()
    
    print(f"\nSummary written to {output_file}")
    print(f"Storage: {storage}")


if __name__ == "__main__":
    main()
