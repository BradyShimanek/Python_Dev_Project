"""
Australian Weather Data Processor

This module reads and processes Australian weather data from CSV files.
It provides functions to load weather data into pandas DataFrames and
store column names in a list for further processing.

Author: Brady Shimanek
Course: Python Development - Spring 2026

NOTE: AI was used to assist in the creation of the documentation for this project. 
"""

import pandas as pd

weather_data = []

def load_weather_data(file_name):
    """
    Load weather data from a CSV file into a pandas DataFrame.

    Args:
        file_name (str): The path to the CSV file containing weather data.

    Returns:
        pandas.DataFrame: A DataFrame containing the weather data.
    """
    content = pd.read_csv(file_name)
    return content

def add_contents_to_weather_data(content):
    """
    Add DataFrame column names to the weather_data list.

    Args:
        content (pandas.DataFrame): The DataFrame whose column names
            will be added to the weather_data list.
    """
    for lines in content:
        weather_data.append(lines)
        
def write_summary_to_file(df, output_file):
    """
    Write a summary of the weather data to a text file.

    Args:
        df (pandas.DataFrame): The weather DataFrame to summarize.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w') as file:
        file.write("=== Weather Data Summary ===\n\n")
        file.write(f"Total records: {len(df)}\n\n")
        file.write(f"Columns: {list(df.columns)}\n\n")
        file.write("Statistical Summary:\n")
        file.write(df.describe().to_string())

if __name__ == "__main__":
    file_name = "data/Weather Training Data.csv"
    content = load_weather_data(file_name)
    add_contents_to_weather_data(content)
    print("Weather Dataframe: ", len(content))
    print(content.describe(), "\n")
    write_summary_to_file(content, "phase_2/weather_summary.txt")
    print("\nMEAN: ")
    print("\nMEDIAN: ")
    print("\nMODE: ")
    print("\nRANGE: ")