"""
Data Visualizer Module

"""

import logging
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

logger = logging.getLogger(__name__)


class DataVisualizer:
    """
    A class for visualizing weather data and performing functional analysis.
    
    Attributes:
        _df (DataFrame): The weather DataFrame to visualize.
    """
    
    def __init__(self, df):
        """
        Initialize the DataVisualizer with a DataFrame.
        
        Args:
            df (pandas.DataFrame): The weather DataFrame to visualize.
        """
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")
        self._df = df
        logger.debug(f"DataVisualizer initialized with {len(df)} records")
    
    # ==================== Filtering Methods ====================
    
    def filter_rainy_days(self):
        """
        Filter data to only include days with rainfall > 0.
        
        Uses: filter() + lambda
        
        Returns:
            pandas.DataFrame: Filtered DataFrame with only rainy days.
        """
        rainy_mask = list(filter(lambda x: x > 0, self._df['Rainfall'].fillna(0)))
        rainy_df = self._df[self._df['Rainfall'] > 0]
        logger.info(f"Filtered to {len(rainy_df)} rainy days")
        return rainy_df
    
    def filter_hot_days(self, threshold=30):
        """
        Filter data to only include days where MaxTemp exceeds threshold.
        
        Uses: filter() + lambda
        
        Args:
            threshold (float): Temperature threshold in Celsius.
        
        Returns:
            pandas.DataFrame: Filtered DataFrame with hot days.
        """
        hot_df = self._df[
            list(map(lambda x: x > threshold, self._df['MaxTemp'].fillna(0)))
        ]
        logger.info(f"Filtered to {len(hot_df)} days above {threshold}°C")
        return hot_df
    
    def map_temp_to_fahrenheit(self, column='MaxTemp'):
        """
        Convert temperature column from Celsius to Fahrenheit.
        
        Uses: map() + lambda
        
        Args:
            column (str): Name of the temperature column.
        
        Returns:
            list: Temperatures converted to Fahrenheit.
        """
        temps_f = list(map(lambda c: c * 9/5 + 32, self._df[column].fillna(0)))
        logger.info(f"Converted {len(temps_f)} temperatures to Fahrenheit")
        return temps_f
    
    def reduce_total_rainfall(self):
        """
        Calculate total rainfall across all records.
        
        Uses: reduce() + lambda
        
        Returns:
            float: Total rainfall.
        """
        rainfall_values = self._df['Rainfall'].fillna(0).tolist()
        total = reduce(lambda acc, x: acc + x, rainfall_values, 0)
        logger.info(f"Total rainfall: {total:.2f}mm")
        return total
    
    def reduce_average_temp(self, column='MaxTemp'):
        """
        Calculate average temperature using reduce.
        
        Uses: reduce() + lambda
        
        Args:
            column (str): Name of the temperature column.
        
        Returns:
            float: Average temperature.
        """
        temps = self._df[column].dropna().tolist()
        if not temps:
            return 0.0
        total = reduce(lambda acc, x: acc + x, temps, 0)
        avg = total / len(temps)
        logger.info(f"Average {column}: {avg:.2f}°C")
        return avg
    
    def get_rainfall_by_location(self):
        """
        Get average rainfall grouped by location.
        
        Uses: filter() to remove NaN values
        
        Returns:
            pandas.Series: Average rainfall by location.
        """
        valid_data = self._df[self._df['Rainfall'].notna()]
        return valid_data.groupby('Location')['Rainfall'].mean().sort_values(ascending=False)
    
    def get_temp_stats_by_location(self):
        """
        Get temperature statistics grouped by location.
        
        Returns:
            pandas.DataFrame: Min, max, mean temps by location.
        """
        return self._df.groupby('Location').agg({
            'MinTemp': 'mean',
            'MaxTemp': 'mean'
        }).round(2)
    
    # ==================== Visualization Methods ====================
    
    def plot_temp_distribution(self, save_path=None):
        """
        Plot histogram of temperature distribution.
        
        Args:
            save_path (str, optional): Path to save the figure.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.histplot(data=self._df, x='MaxTemp', kde=True, ax=ax, color='coral')
        ax.set_title('Distribution of Maximum Temperatures')
        ax.set_xlabel('Maximum Temperature (°C)')
        ax.set_ylabel('Frequency')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved temperature distribution plot to {save_path}")
        plt.show()
    
    def plot_rainfall_by_location(self, top_n=10, save_path=None):
        """
        Plot bar chart of average rainfall by location.
        
        Args:
            top_n (int): Number of top locations to show.
            save_path (str, optional): Path to save the figure.
        """
        rainfall_by_loc = self.get_rainfall_by_location().head(top_n)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        sns.barplot(x=rainfall_by_loc.values, y=rainfall_by_loc.index, ax=ax, palette='Blues_d')
        ax.set_title(f'Top {top_n} Locations by Average Rainfall')
        ax.set_xlabel('Average Rainfall (mm)')
        ax.set_ylabel('Location')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved rainfall by location plot to {save_path}")
        plt.show()
    
    def plot_temp_trends(self, sample_size=1000, save_path=None):
        """
        Plot line chart of temperature trends.
        
        Args:
            sample_size (int): Number of records to sample for clarity.
            save_path (str, optional): Path to save the figure.
        """
        sample_df = self._df.head(sample_size)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(range(len(sample_df)), sample_df['MaxTemp'], label='Max Temp', color='red', alpha=0.7)
        ax.plot(range(len(sample_df)), sample_df['MinTemp'], label='Min Temp', color='blue', alpha=0.7)
        ax.fill_between(range(len(sample_df)), sample_df['MinTemp'], sample_df['MaxTemp'], alpha=0.2)
        
        ax.set_title('Temperature Trends (Min and Max)')
        ax.set_xlabel('Record Index')
        ax.set_ylabel('Temperature (°C)')
        ax.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved temperature trends plot to {save_path}")
        plt.show()
    
    def plot_correlation_heatmap(self, save_path=None):
        """
        Plot heatmap showing correlation between numeric variables.
        
        Args:
            save_path (str, optional): Path to save the figure.
        """
        numeric_df = self._df.select_dtypes(include='number')
        corr_matrix = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    fmt='.2f', ax=ax, square=True)
        ax.set_title('Correlation Heatmap of Weather Variables')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved correlation heatmap to {save_path}")
        plt.show()
    
    def plot_rainy_vs_dry_days(self, save_path=None):
        """
        Plot pie chart comparing rainy vs dry days.
        
        Args:
            save_path (str, optional): Path to save the figure.
        """
        rainy_count = len(self._df[self._df['Rainfall'] > 0])
        dry_count = len(self._df[self._df['Rainfall'] == 0])
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        ax.pie([rainy_count, dry_count], 
               labels=['Rainy Days', 'Dry Days'],
               autopct='%1.1f%%',
               colors=['steelblue', 'lightyellow'],
               explode=(0.05, 0))
        ax.set_title('Proportion of Rainy vs Dry Days')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Saved rainy vs dry days plot to {save_path}")
        plt.show()
    
    def __str__(self):
        """String representation of the DataVisualizer."""
        return f"DataVisualizer(records={len(self._df)})"
    
    def __repr__(self):
        """Developer representation of the DataVisualizer."""
        return f"DataVisualizer(df=DataFrame({len(self._df)} rows))"
