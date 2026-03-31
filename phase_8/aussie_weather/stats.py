"""
Data Processor Module

Class for calculating descriptive statistics on weather data.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def compute_stats_string(df):
    """Compute descriptive statistics and return as a formatted string. Used by multiprocessing workers."""
    proc = DataProcessor(df)
    lines = ["\n=== Descriptive Statistics ===\n"]
    for stat_name, stat_values in proc.generate_stats():
        lines.append(f"{stat_name.upper()}:")
        if stat_values is not None:
            lines.append(stat_values.to_string())
        else:
            lines.append("N/A")
        lines.append("")
    return "\n".join(lines)


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
        
        Raises:
            ValueError: If the DataFrame is None or empty.
            TypeError: If the input is not a DataFrame.
        """
        if df is None:
            logger.error("Attempted to create DataProcessor with None")
            raise ValueError("DataFrame cannot be None")
        if not isinstance(df, pd.DataFrame):
            logger.error(f"Invalid type passed to DataProcessor: {type(df).__name__}")
            raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")
        if df.empty:
            logger.error("Attempted to create DataProcessor with empty DataFrame")
            raise ValueError("DataFrame is empty")
        
        self._df = df
        self._stats = None
        logger.debug(f"DataProcessor initialized with {len(df)} records")
    
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
    
    def generate_stats(self):
        """
        Generator that yields statistics one at a time.
        
        Yields:
            tuple: (stat_name, stat_values) for each statistic.
        """
        numeric_df = self.numeric_data
        
        yield ('mean', numeric_df.mean())
        yield ('median', numeric_df.median())
        yield ('mode', numeric_df.mode().iloc[0] if not numeric_df.mode().empty else None)
        yield ('std', numeric_df.std())
        yield ('min', numeric_df.min())
        yield ('max', numeric_df.max())
        yield ('range', numeric_df.max() - numeric_df.min())
        yield ('count', numeric_df.count())
    
    def print_stats(self):
        """Print formatted descriptive statistics to console."""
        print("\n=== Descriptive Statistics ===\n")
        print(compute_stats_string(self._df))

    def __str__(self):
        """String representation of the DataProcessor."""
        return f"DataProcessor(records={len(self._df)}, numeric_columns={len(self.numeric_data.columns)})"
    
    def __repr__(self):
        """Developer representation of the DataProcessor."""
        return f"DataProcessor(df=DataFrame({len(self._df)} rows))"
