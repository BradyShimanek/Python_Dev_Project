"""
Main Entry Point

Demonstrates the usage of the aussie_weather package.

Author: Brady Shimanek
Course: Python Development - Spring 2026

NOTE: AI was used to assist in the creation of the documentation for this project.
"""

from aussie_weather import (
    load_weather_data,
    print_descriptive_stats,
    write_summary_to_file
)


def main():
    """Main function to run the weather data analysis."""
    # Load the weather data
    file_name = "data/Weather Training Data.csv"
    df = load_weather_data(file_name)
    
    print(f"Loaded {len(df)} weather records.\n")
    
    # Print descriptive statistics
    print_descriptive_stats(df)
    
    # Write summary to file
    output_file = "phase_2/weather_summary.txt"
    write_summary_to_file(df, output_file)
    print(f"\nSummary written to {output_file}")


if __name__ == "__main__":
    main()

