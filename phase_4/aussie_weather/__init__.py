"""
Aussie Weather Package

A Python package for loading, analyzing, and processing Australian weather data.

Author: Brady S
Course: Python Development - Spring 2026
"""

from .loader import DataFetcher
from .stats import DataProcessor
from .writer import DataStorage

__version__ = "0.2.0"
__all__ = [
    "DataFetcher",
    "DataProcessor", 
    "DataStorage"
]
