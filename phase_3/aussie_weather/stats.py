"""
Data Processor Module

Class for calculating descriptive statistics on weather data.
"""

import pandas as pd


class DataProcessor:
    """
    A class for processing weather data and calculating statistics.
    
    Attributes:
        _df (DataFrame): The weather DataFrame to process.
        _stats (dict): Cached statistics results.
    """
    
    def __init__(self, df):
        """
        Initialize the DataProcessor with a DataFrame.
        
        Args:
            df (pandas.DataFrame): The weather DataFrame to analyze.
        """
        self._df = df
        self._stats = None
    
    @property
    def numeric_data(self):
        """Get only the numeric columns from the DataFrame."""
        return self._df.select_dtypes(include='number')
    
    @property
    def stats(self):
        """
        Get descriptive statistics. Calculates if not already cached.
        
        Returns:
            dict: Dictionary containing mean, median, mode, std, min, max, range, count.
        """
        if self._stats is None:
            self._stats = self._calculate_stats()
        return self._stats
    
    def _calculate_stats(self):
        """
        Calculate descriptive statistics for numeric columns.
        
        Returns:
            dict: A dictionary containing descriptive statistics.
        """
        numeric_df = self.numeric_data
        
        return {
            'mean': numeric_df.mean(),
            'median': numeric_df.median(),
            'mode': numeric_df.mode().iloc[0] if not numeric_df.mode().empty else None,
            'std': numeric_df.std(),
            'min': numeric_df.min(),
            'max': numeric_df.max(),
            'range': numeric_df.max() - numeric_df.min(),
            'count': numeric_df.count()
        }
    
    def print_stats(self):
        """Print formatted descriptive statistics to console."""
        stats = self.stats
        
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
    
    def __str__(self):
        """String representation of the DataProcessor."""
        return f"DataProcessor(records={len(self._df)}, numeric_columns={len(self.numeric_data.columns)})"
    
    def __repr__(self):
        """Developer representation of the DataProcessor."""
        return f"DataProcessor(df=DataFrame({len(self._df)} rows))"
