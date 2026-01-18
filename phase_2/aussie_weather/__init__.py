"""
Aussie Weather Package

A Python package for loading, analyzing, and processing Australian weather data.

Author: Brady Shimanek
Course: Python Development - Spring 2026
"""

from .loader import load_weather_data
from .stats import get_descriptive_stats, print_descriptive_stats
from .writer import write_summary_to_file

__version__ = "0.1.0"
__all__ = [
    "load_weather_data",
    "get_descriptive_stats",
    "print_descriptive_stats",
    "write_summary_to_file"
]

