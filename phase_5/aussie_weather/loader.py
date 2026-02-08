"""
Data Fetcher Module

Class for loading weather data from CSV files.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataFetcher:
    """
    A class for fetching and loading weather data from CSV files.
    
    Attributes:
        file_path (str): Path to the CSV file.
        _data (DataFrame): The loaded weather data.
        _iter_index (int): Current index for iteration.
    """
    
    def __init__(self, file_path):
        """
        Initialize the DataFetcher with a file path.
        
        Args:
            file_path (str): Path to the CSV file containing weather data.
        """
        self.file_path = file_path
        self._data = None
        self._iter_index = 0
    
    def load(self):
        """
        Load weather data from the CSV file.
        
        Returns:
            pandas.DataFrame: The loaded weather data.
        
        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the file is empty or has invalid format.
        """
        logger.debug(f"Attempting to load file: {self.file_path}")
        try:
            self._data = pd.read_csv(self.file_path)
            if self._data.empty:
                logger.warning(f"File is empty: {self.file_path}")
                raise ValueError(f"The file '{self.file_path}' is empty")
            logger.info(f"Successfully loaded {len(self._data)} records from {self.file_path}")
            return self._data
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"Could not find file: '{self.file_path}'")
        except pd.errors.EmptyDataError:
            logger.error(f"Empty data error: {self.file_path}")
            raise ValueError(f"The file '{self.file_path}' is empty or has no valid data")
        except pd.errors.ParserError as e:
            logger.error(f"Parser error for {self.file_path}: {e}")
            raise ValueError(f"Error parsing CSV file '{self.file_path}': {e}")
    
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
    
    def __iter__(self):
        """
        Initialize iteration over the weather data rows.
        
        Returns:
            DataFetcher: The iterator object (self).
        """
        self._iter_index = 0
        return self
    
    def __next__(self):
        """
        Get the next row of weather data.
        
        Returns:
            pandas.Series: The next row of data.
        
        Raises:
            StopIteration: When all rows have been iterated.
        """
        if self._iter_index < len(self.data):
            row = self.data.iloc[self._iter_index]
            self._iter_index += 1
            return row
        else:
            raise StopIteration
