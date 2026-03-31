"""
Data Storage Module

Class for writing weather data and statistics to files.
"""

import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """
    A class for storing and writing weather data summaries to files.
    
    Attributes:
        _df (DataFrame): The weather DataFrame to summarize.
        output_path (str): Path to the output file.
    """
    
    def __init__(self, df, output_path=None):
        """
        Initialize the DataStorage with a DataFrame.
        
        Args:
            df (pandas.DataFrame): The weather DataFrame to summarize.
            output_path (str, optional): Default output file path.
        """
        self._df = df
        self.output_path = output_path
    
    def write_summary(self, output_path=None):
        """
        Write a summary of the weather data to a text file.
        
        Args:
            output_path (str, optional): Path to output file. 
                Uses default output_path if not provided.
        
        Returns:
            str: The path where the file was written.
        
        Raises:
            ValueError: If no output path is specified.
            IOError: If the file cannot be written.
        """
        path = output_path or self.output_path
        if path is None:
            logger.error("No output path specified for write_summary")
            raise ValueError("No output path specified")
        
        logger.debug(f"Writing summary to {path}")
        try:
            with open(path, 'w') as file:
                file.write("=== Weather Data Summary ===\n\n")
                file.write(f"Total records: {len(self._df)}\n\n")
                file.write(f"Columns: {list(self._df.columns)}\n\n")
                file.write("Statistical Summary:\n")
                file.write(self._df.describe().T.round(2).to_string())
            logger.info(f"Successfully wrote summary to {path}")
            return path
        except PermissionError:
            logger.error(f"Permission denied writing to {path}")
            raise IOError(f"Permission denied: Cannot write to '{path}'")
        except OSError as e:
            logger.error(f"OS error writing to {path}: {e}")
            raise IOError(f"Error writing to file '{path}': {e}")
    
    def __str__(self):
        """String representation of the DataStorage."""
        return f"DataStorage(records={len(self._df)}, output='{self.output_path}')"
    
    def __repr__(self):
        """Developer representation of the DataStorage."""
        return f"DataStorage(df=DataFrame({len(self._df)} rows), output_path='{self.output_path}')"
