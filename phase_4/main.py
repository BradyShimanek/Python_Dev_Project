"""
Main Entry Point

Demonstrates the usage of the aussie_weather package.

Author: Brady S
Course: Python Development - Spring 2026

NOTE: AI was used to assist in the creation of the documentation for this project.
"""

import logging
from aussie_weather import DataFetcher, DataProcessor, DataStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the weather data analysis."""
    
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
        
        storage = DataStorage(fetcher.data, "phase_4/weather_summary.txt")
        output_file = storage.write_summary()
        logger.info(f"Summary written to {output_file}")
        
        print(f"\nSummary written to {output_file}")
        print(f"Storage: {storage}")
        
        logger.info("Weather data analysis completed successfully")
        
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
