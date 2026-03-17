"""
Unit tests for the DataFetcher class.
"""

import unittest
import tempfile
import os
import pandas as pd
from aussie_weather.loader import DataFetcher


class TestDataFetcher(unittest.TestCase):
    """Test cases for DataFetcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.valid_csv_path = os.path.join(self.temp_dir, "test_data.csv")
        self.empty_csv_path = os.path.join(self.temp_dir, "empty.csv")
        self.invalid_csv_path = os.path.join(self.temp_dir, "invalid.csv")
        
        # Create valid test CSV
        self.test_data = pd.DataFrame({
            'Location': ['Sydney', 'Melbourne', 'Brisbane'],
            'MinTemp': [10.5, 8.2, 15.3],
            'MaxTemp': [25.0, 22.5, 30.1],
            'Rainfall': [0.0, 2.5, 0.0]
        })
        self.test_data.to_csv(self.valid_csv_path, index=False)
        
        # Create empty CSV
        with open(self.empty_csv_path, 'w') as f:
            f.write("")
        
        # Create invalid CSV
        with open(self.invalid_csv_path, 'w') as f:
            f.write("col1,col2\n1,2,3,4,5\n")
    
    def tearDown(self):
        """Clean up test files."""
        for file in [self.valid_csv_path, self.empty_csv_path, self.invalid_csv_path]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)
    
    def test_load_valid_csv(self):
        """Test loading a valid CSV file."""
        fetcher = DataFetcher(self.valid_csv_path)
        data = fetcher.load()
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)
    
    def test_load_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        fetcher = DataFetcher("nonexistent_file.csv")
        
        with self.assertRaises(FileNotFoundError):
            fetcher.load()
    
    def test_load_empty_file(self):
        """Test that ValueError is raised for empty file."""
        fetcher = DataFetcher(self.empty_csv_path)
        
        with self.assertRaises(ValueError):
            fetcher.load()
    
    def test_data_property_lazy_loads(self):
        """Test that data property triggers lazy loading."""
        fetcher = DataFetcher(self.valid_csv_path)
        
        self.assertIsNone(fetcher._data)
        data = fetcher.data
        self.assertIsNotNone(fetcher._data)
        self.assertEqual(len(data), 3)
    
    def test_record_count(self):
        """Test record_count property returns correct count."""
        fetcher = DataFetcher(self.valid_csv_path)
        fetcher.load()
        
        self.assertEqual(fetcher.record_count, 3)
    
    def test_columns(self):
        """Test columns property returns correct column names."""
        fetcher = DataFetcher(self.valid_csv_path)
        fetcher.load()
        
        expected_columns = ['Location', 'MinTemp', 'MaxTemp', 'Rainfall']
        self.assertEqual(fetcher.columns, expected_columns)
    
    def test_iterator(self):
        """Test that DataFetcher is iterable."""
        fetcher = DataFetcher(self.valid_csv_path)
        fetcher.load()
        
        rows = list(fetcher)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['Location'], 'Sydney')
    
    def test_iterator_resets(self):
        """Test that iterator resets on each iteration."""
        fetcher = DataFetcher(self.valid_csv_path)
        fetcher.load()
        
        first_pass = list(fetcher)
        second_pass = list(fetcher)
        
        self.assertEqual(len(first_pass), len(second_pass))
    
    def test_str_representation(self):
        """Test __str__ returns expected format."""
        fetcher = DataFetcher(self.valid_csv_path)
        fetcher.load()
        
        str_repr = str(fetcher)
        self.assertIn("DataFetcher", str_repr)
        self.assertIn("records=3", str_repr)
    
    def test_repr_representation(self):
        """Test __repr__ returns expected format."""
        fetcher = DataFetcher(self.valid_csv_path)
        
        repr_str = repr(fetcher)
        self.assertIn("DataFetcher", repr_str)
        self.assertIn("file_path=", repr_str)


if __name__ == '__main__':
    unittest.main()
