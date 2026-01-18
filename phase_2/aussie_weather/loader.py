"""
Data Loading Module

Functions for loading weather data from CSV files.
"""

import pandas as pd


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

