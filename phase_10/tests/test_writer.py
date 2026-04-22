"""
Unit tests for the DataStorage class.
"""

import unittest
import tempfile
import os
import pandas as pd
from unittest.mock import patch, mock_open
from aussie_weather.writer import DataStorage


class TestDataStorage(unittest.TestCase):
    """Test cases for DataStorage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_df = pd.DataFrame({
            'Location': ['Sydney', 'Melbourne', 'Brisbane'],
            'MinTemp': [10.0, 8.0, 15.0],
            'MaxTemp': [25.0, 22.0, 30.0],
            'Rainfall': [0.0, 2.0, 0.0]
        })
        
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "test_summary.txt")
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_init_with_dataframe(self):
        """Test initialization with DataFrame."""
        storage = DataStorage(self.test_df)
        
        self.assertIsNotNone(storage._df)
        self.assertIsNone(storage.output_path)
    
    def test_init_with_output_path(self):
        """Test initialization with DataFrame and output path."""
        storage = DataStorage(self.test_df, self.output_path)
        
        self.assertEqual(storage.output_path, self.output_path)
    
    def test_write_summary_success(self):
        """Test successful file writing."""
        storage = DataStorage(self.test_df, self.output_path)
        result = storage.write_summary()
        
        self.assertEqual(result, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
    
    def test_write_summary_with_override_path(self):
        """Test writing with overridden output path."""
        storage = DataStorage(self.test_df, "original_path.txt")
        result = storage.write_summary(self.output_path)
        
        self.assertEqual(result, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
    
    def test_write_summary_no_path_raises(self):
        """Test that ValueError is raised when no path specified."""
        storage = DataStorage(self.test_df)
        
        with self.assertRaises(ValueError) as context:
            storage.write_summary()
        
        self.assertIn("No output path", str(context.exception))
    
    def test_write_summary_content_header(self):
        """Test that written file contains expected header."""
        storage = DataStorage(self.test_df, self.output_path)
        storage.write_summary()
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("=== Weather Data Summary ===", content)
    
    def test_write_summary_content_record_count(self):
        """Test that written file contains record count."""
        storage = DataStorage(self.test_df, self.output_path)
        storage.write_summary()
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("Total records: 3", content)
    
    def test_write_summary_content_columns(self):
        """Test that written file contains column names."""
        storage = DataStorage(self.test_df, self.output_path)
        storage.write_summary()
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("Columns:", content)
        self.assertIn("Location", content)
        self.assertIn("MinTemp", content)
    
    def test_write_summary_content_statistics(self):
        """Test that written file contains statistical summary."""
        storage = DataStorage(self.test_df, self.output_path)
        storage.write_summary()
        
        with open(self.output_path, 'r') as f:
            content = f.read()
        
        self.assertIn("Statistical Summary:", content)
    
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_write_summary_permission_error(self, mock_file):
        """Test that IOError is raised on permission error."""
        storage = DataStorage(self.test_df, "/protected/path.txt")
        
        with self.assertRaises(IOError) as context:
            storage.write_summary()
        
        self.assertIn("Permission denied", str(context.exception))
    
    def test_str_representation(self):
        """Test __str__ returns expected format."""
        storage = DataStorage(self.test_df, self.output_path)
        str_repr = str(storage)
        
        self.assertIn("DataStorage", str_repr)
        self.assertIn("records=3", str_repr)
    
    def test_repr_representation(self):
        """Test __repr__ returns expected format."""
        storage = DataStorage(self.test_df, self.output_path)
        repr_str = repr(storage)
        
        self.assertIn("DataStorage", repr_str)
        self.assertIn("3 rows", repr_str)


if __name__ == '__main__':
    unittest.main()
