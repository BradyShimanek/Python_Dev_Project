"""
Unit tests for the DataVisualizer class.

"""

import unittest
import pandas as pd
from aussie_weather.visualizer import DataVisualizer


class TestDataVisualizer(unittest.TestCase):
    """Test cases for DataVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_df = pd.DataFrame({
            'Location': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'MinTemp': [10.0, 8.0, 15.0, 12.0, 9.0],
            'MaxTemp': [25.0, 22.0, 32.0, 28.0, 20.0],
            'Rainfall': [0.0, 2.5, 0.0, 5.0, 0.0]
        })
    
    def test_init_valid_dataframe(self):
        """Test initialization with valid DataFrame."""
        viz = DataVisualizer(self.test_df)
        self.assertIsNotNone(viz._df)
    
    def test_init_none_raises(self):
        """Test that None DataFrame raises ValueError."""
        with self.assertRaises(ValueError):
            DataVisualizer(None)
    
    def test_init_empty_raises(self):
        """Test that empty DataFrame raises ValueError."""
        with self.assertRaises(ValueError):
            DataVisualizer(pd.DataFrame())
    
    def test_filter_rainy_days(self):
        """Test filtering for rainy days using filter() and lambda."""
        viz = DataVisualizer(self.test_df)
        rainy = viz.filter_rainy_days()
        
        self.assertEqual(len(rainy), 2)
        self.assertTrue(all(rainy['Rainfall'] > 0))
    
    def test_filter_hot_days(self):
        """Test filtering for hot days using map() and lambda."""
        viz = DataVisualizer(self.test_df)
        hot = viz.filter_hot_days(threshold=25)
        
        self.assertEqual(len(hot), 2)
        self.assertTrue(all(hot['MaxTemp'] > 25))
    
    def test_filter_hot_days_custom_threshold(self):
        """Test filtering with custom temperature threshold."""
        viz = DataVisualizer(self.test_df)
        hot = viz.filter_hot_days(threshold=30)
        
        self.assertEqual(len(hot), 1)
        self.assertEqual(hot.iloc[0]['Location'], 'Brisbane')
    
    def test_map_temp_to_fahrenheit(self):
        """Test temperature conversion using map() and lambda."""
        viz = DataVisualizer(self.test_df)
        temps_f = viz.map_temp_to_fahrenheit('MaxTemp')
        
        self.assertEqual(len(temps_f), 5)
        self.assertAlmostEqual(temps_f[0], 77.0)  # 25°C = 77°F
        self.assertAlmostEqual(temps_f[2], 89.6)  # 32°C = 89.6°F
    
    def test_reduce_total_rainfall(self):
        """Test total rainfall calculation using reduce() and lambda."""
        viz = DataVisualizer(self.test_df)
        total = viz.reduce_total_rainfall()
        
        self.assertAlmostEqual(total, 7.5)
    
    def test_reduce_average_temp(self):
        """Test average temperature calculation using reduce() and lambda."""
        viz = DataVisualizer(self.test_df)
        avg = viz.reduce_average_temp('MaxTemp')
        
        expected = (25 + 22 + 32 + 28 + 20) / 5
        self.assertAlmostEqual(avg, expected)
    
    def test_get_rainfall_by_location(self):
        """Test grouping rainfall by location."""
        viz = DataVisualizer(self.test_df)
        rainfall = viz.get_rainfall_by_location()
        
        self.assertEqual(rainfall['Perth'], 5.0)
        self.assertEqual(rainfall['Melbourne'], 2.5)
    
    def test_get_temp_stats_by_location(self):
        """Test temperature statistics by location."""
        viz = DataVisualizer(self.test_df)
        stats = viz.get_temp_stats_by_location()
        
        self.assertIn('MinTemp', stats.columns)
        self.assertIn('MaxTemp', stats.columns)
        self.assertEqual(stats.loc['Sydney', 'MaxTemp'], 25.0)
    
    def test_str_representation(self):
        """Test __str__ returns expected format."""
        viz = DataVisualizer(self.test_df)
        str_repr = str(viz)
        
        self.assertIn("DataVisualizer", str_repr)
        self.assertIn("records=5", str_repr)
    
    def test_repr_representation(self):
        """Test __repr__ returns expected format."""
        viz = DataVisualizer(self.test_df)
        repr_str = repr(viz)
        
        self.assertIn("DataVisualizer", repr_str)
        self.assertIn("5 rows", repr_str)


class TestFunctionalProgrammingConcepts(unittest.TestCase):
    """Test cases specifically verifying functional programming usage."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_df = pd.DataFrame({
            'Location': ['A', 'B', 'C', 'D'],
            'MinTemp': [5.0, 10.0, 15.0, 20.0],
            'MaxTemp': [20.0, 25.0, 30.0, 35.0],
            'Rainfall': [0.0, 1.0, 2.0, 3.0]
        })
    
    def test_filter_returns_correct_subset(self):
        """Verify filter() correctly subsets data."""
        viz = DataVisualizer(self.test_df)
        rainy = viz.filter_rainy_days()
        
        self.assertEqual(list(rainy['Location']), ['B', 'C', 'D'])
    
    def test_map_applies_transformation(self):
        """Verify map() applies transformation to all elements."""
        viz = DataVisualizer(self.test_df)
        temps_f = viz.map_temp_to_fahrenheit('MinTemp')
        
        expected = [41.0, 50.0, 59.0, 68.0]
        for actual, exp in zip(temps_f, expected):
            self.assertAlmostEqual(actual, exp)
    
    def test_reduce_aggregates_correctly(self):
        """Verify reduce() aggregates values correctly."""
        viz = DataVisualizer(self.test_df)
        total = viz.reduce_total_rainfall()
        
        self.assertEqual(total, 6.0)


if __name__ == '__main__':
    unittest.main()
