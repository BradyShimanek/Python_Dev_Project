"""
Data Fetcher Module

Class for loading weather data from CSV files.
"""

import pandas as pd


class DataFetcher:
    """
    A class for fetching and loading weather data from CSV files.
    
    Attributes:
        file_path (str): Path to the CSV file.
        _data (DataFrame): The loaded weather data.
    """
    
    def __init__(self, file_path):
        """
        Initialize the DataFetcher with a file path.
        
        Args:
            file_path (str): Path to the CSV file containing weather data.
        """
        self.file_path = file_path
        self._data = None
    
    def load(self):
        """
        Load weather data from the CSV file.
        
        Returns:
            pandas.DataFrame: The loaded weather data.
        """
        self._data = pd.read_csv(self.file_path)
        return self._data
    
    @property
    def data(self):
        """
        Get the loaded data. Loads automatically if not already loaded.
        
        Returns:
            pandas.DataFrame: The weather data.
        """
        if self._data is None:
            self.load()
        return self._data
    
    @property
    def record_count(self):
        """Get the number of records in the dataset."""
        return len(self.data) if self._data is not None else 0
    
    @property
    def columns(self):
        """Get the column names of the dataset."""
        return list(self.data.columns) if self._data is not None else []
    
    def __str__(self):
        """String representation of the DataFetcher."""
        return f"DataFetcher(file='{self.file_path}', records={self.record_count})"
    
    def __repr__(self):
        """Developer representation of the DataFetcher."""
        return f"DataFetcher(file_path='{self.file_path}')"
