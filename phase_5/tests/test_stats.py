"""
Unit tests for the DataProcessor class.
"""

import unittest
import pandas as pd
from aussie_weather.stats import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_df = pd.DataFrame({
            'Location': ['Sydney', 'Melbourne', 'Brisbane', 'Perth'],
            'MinTemp': [10.0, 8.0, 15.0, 12.0],
            'MaxTemp': [25.0, 22.0, 30.0, 28.0],
            'Rainfall': [0.0, 2.0, 0.0, 1.0]
        })
        
        self.numeric_only_df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [10, 20, 30, 40]
        })
    
    def test_init_valid_dataframe(self):
        """Test initialization with valid DataFrame."""
        processor = DataProcessor(self.test_df)
        
        self.assertIsNotNone(processor._df)
        self.assertEqual(len(processor._df), 4)
    
    def test_init_none_raises_value_error(self):
        """Test that None DataFrame raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DataProcessor(None)
        
        self.assertIn("None", str(context.exception))
    
    def test_init_wrong_type_raises_type_error(self):
        """Test that non-DataFrame raises TypeError."""
        with self.assertRaises(TypeError) as context:
            DataProcessor([1, 2, 3])
        
        self.assertIn("list", str(context.exception))
    
    def test_init_empty_dataframe_raises_value_error(self):
        """Test that empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()
        
        with self.assertRaises(ValueError) as context:
            DataProcessor(empty_df)
        
        self.assertIn("empty", str(context.exception))
    
    def test_numeric_data_filters_correctly(self):
        """Test that numeric_data property filters non-numeric columns."""
        processor = DataProcessor(self.test_df)
        numeric = processor.numeric_data
        
        self.assertNotIn('Location', numeric.columns)
        self.assertIn('MinTemp', numeric.columns)
        self.assertIn('MaxTemp', numeric.columns)
        self.assertIn('Rainfall', numeric.columns)
    
    def test_generate_stats_yields_all_stats(self):
        """Test that generate_stats yields all 8 statistics."""
        processor = DataProcessor(self.numeric_only_df)
        
        stats_list = list(processor.generate_stats())
        stat_names = [name for name, _ in stats_list]
        
        self.assertEqual(len(stats_list), 8)
        self.assertIn('mean', stat_names)
        self.assertIn('median', stat_names)
        self.assertIn('mode', stat_names)
        self.assertIn('std', stat_names)
        self.assertIn('min', stat_names)
        self.assertIn('max', stat_names)
        self.assertIn('range', stat_names)
        self.assertIn('count', stat_names)
    
    def test_generate_stats_is_generator(self):
        """Test that generate_stats returns a generator."""
        processor = DataProcessor(self.test_df)
        gen = processor.generate_stats()
        
        import types
        self.assertIsInstance(gen, types.GeneratorType)
    
    def test_stats_property_returns_dict(self):
        """Test that stats property returns dictionary."""
        processor = DataProcessor(self.test_df)
        stats = processor.stats
        
        self.assertIsInstance(stats, dict)
        self.assertIn('mean', stats)
        self.assertIn('median', stats)
    
    def test_stats_property_caches_result(self):
        """Test that stats property caches the result."""
        processor = DataProcessor(self.test_df)
        
        self.assertIsNone(processor._stats)
        _ = processor.stats
        self.assertIsNotNone(processor._stats)
    
    def test_mean_calculation(self):
        """Test that mean is calculated correctly."""
        processor = DataProcessor(self.numeric_only_df)
        stats = processor.stats
        
        self.assertEqual(stats['mean']['A'], 2.5)
        self.assertEqual(stats['mean']['B'], 25.0)
    
    def test_median_calculation(self):
        """Test that median is calculated correctly."""
        processor = DataProcessor(self.numeric_only_df)
        stats = processor.stats
        
        self.assertEqual(stats['median']['A'], 2.5)
        self.assertEqual(stats['median']['B'], 25.0)
    
    def test_min_max_calculation(self):
        """Test that min and max are calculated correctly."""
        processor = DataProcessor(self.numeric_only_df)
        stats = processor.stats
        
        self.assertEqual(stats['min']['A'], 1)
        self.assertEqual(stats['max']['A'], 4)
        self.assertEqual(stats['min']['B'], 10)
        self.assertEqual(stats['max']['B'], 40)
    
    def test_range_calculation(self):
        """Test that range (max - min) is calculated correctly."""
        processor = DataProcessor(self.numeric_only_df)
        stats = processor.stats
        
        self.assertEqual(stats['range']['A'], 3)
        self.assertEqual(stats['range']['B'], 30)
    
    def test_str_representation(self):
        """Test __str__ returns expected format."""
        processor = DataProcessor(self.test_df)
        str_repr = str(processor)
        
        self.assertIn("DataProcessor", str_repr)
        self.assertIn("records=4", str_repr)
    
    def test_repr_representation(self):
        """Test __repr__ returns expected format."""
        processor = DataProcessor(self.test_df)
        repr_str = repr(processor)
        
        self.assertIn("DataProcessor", repr_str)
        self.assertIn("4 rows", repr_str)


if __name__ == '__main__':
    unittest.main()
