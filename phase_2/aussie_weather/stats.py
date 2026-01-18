"""
Statistics Module

Functions for calculating descriptive statistics on weather data.
"""

import pandas as pd


def get_descriptive_stats(df):
    """
    Calculate descriptive statistics for the weather DataFrame.

    Includes: mean, median, mode, range, std, min, max, etc.

    Args:
        df (pandas.DataFrame): The weather DataFrame to analyze.

    Returns:
        dict: A dictionary containing descriptive statistics.
    """
    # Select only numeric columns for statistics
    numeric_df = df.select_dtypes(include='number')
    
    stats = {
        'mean': numeric_df.mean(),
        'median': numeric_df.median(),
        'mode': numeric_df.mode().iloc[0] if not numeric_df.mode().empty else None,
        'std': numeric_df.std(),
        'min': numeric_df.min(),
        'max': numeric_df.max(),
        'range': numeric_df.max() - numeric_df.min(),
        'count': numeric_df.count()
    }
    return stats


def print_descriptive_stats(df):
    """
    Print descriptive statistics for the weather DataFrame.

    Args:
        df (pandas.DataFrame): The weather DataFrame to analyze.
    """
    stats = get_descriptive_stats(df)
    
    print("\n=== Descriptive Statistics ===\n")
    print("MEAN:")
    print(stats['mean'].to_string())
    print("\nMEDIAN:")
    print(stats['median'].to_string())
    print("\nMODE:")
    print(stats['mode'].to_string() if stats['mode'] is not None else "N/A")
    print("\nRANGE (max - min):")
    print(stats['range'].to_string())
    print("\nSTANDARD DEVIATION:")
    print(stats['std'].to_string())

