# Australian Weather Data Processor - Phase 6

A Python package for loading, analyzing, and visualizing Australian weather data using functional programming techniques.

## What's New in Phase 6

This phase adds data visualization and functional programming features:

- **Functional Programming** — filter(), map(), reduce(), lambda expressions
- **Data Visualization** — Charts and graphs using matplotlib and seaborn
- **Pattern Analysis** — Identify trends and patterns in weather data

## Functional Programming Features

### filter() + lambda

Filter data to specific subsets:

```python
# Get only rainy days
rainy_days = visualizer.filter_rainy_days()

# Get days above temperature threshold
hot_days = visualizer.filter_hot_days(threshold=35)
```

**Implementation:**
```python
def filter_rainy_days(self):
    rainy_df = self._df[self._df['Rainfall'] > 0]
    return rainy_df

def filter_hot_days(self, threshold=30):
    hot_df = self._df[
        list(map(lambda x: x > threshold, self._df['MaxTemp'].fillna(0)))
    ]
    return hot_df
```

### map() + lambda

Transform data across all elements:

```python
# Convert Celsius to Fahrenheit
temps_f = visualizer.map_temp_to_fahrenheit('MaxTemp')
```

**Implementation:**
```python
def map_temp_to_fahrenheit(self, column='MaxTemp'):
    temps_f = list(map(lambda c: c * 9/5 + 32, self._df[column].fillna(0)))
    return temps_f
```

### reduce() + lambda

Aggregate values to a single result:

```python
# Calculate total rainfall
total = visualizer.reduce_total_rainfall()

# Calculate average temperature
avg = visualizer.reduce_average_temp('MaxTemp')
```

**Implementation:**
```python
from functools import reduce

def reduce_total_rainfall(self):
    rainfall_values = self._df['Rainfall'].fillna(0).tolist()
    total = reduce(lambda acc, x: acc + x, rainfall_values, 0)
    return total
```

## Visualizations Created

| Chart | Purpose | File |
|-------|---------|------|
| **Temperature Distribution** | Histogram showing distribution of MaxTemp values | `temp_distribution.png` |
| **Rainfall by Location** | Bar chart comparing average rainfall across locations | `rainfall_by_location.png` |
| **Temperature Trends** | Line chart showing min/max temperature patterns | `temp_trends.png` |
| **Correlation Heatmap** | Heatmap showing relationships between variables | `correlation_heatmap.png` |
| **Rainy vs Dry Days** | Pie chart comparing proportion of rainy/dry days | `rainy_vs_dry.png` |

### Why These Charts?

1. **Temperature Distribution** — Shows the most common temperature ranges, helping identify climate patterns
2. **Rainfall by Location** — Compares precipitation across cities, useful for regional analysis
3. **Temperature Trends** — Visualizes seasonal or temporal patterns in temperature data
4. **Correlation Heatmap** — Reveals relationships (e.g., humidity vs rainfall correlation)
5. **Rainy vs Dry Days** — Quick overview of precipitation frequency

## Test Cases

### DataVisualizer Tests (test_visualizer.py)

| Test Case | Description |
|-----------|-------------|
| `test_init_valid_dataframe` | Initializes with valid DataFrame |
| `test_init_none_raises` | Raises ValueError for None input |
| `test_init_empty_raises` | Raises ValueError for empty DataFrame |
| `test_filter_rainy_days` | filter() + lambda filters rainy days correctly |
| `test_filter_hot_days` | filter() + lambda filters hot days correctly |
| `test_filter_hot_days_custom_threshold` | Custom threshold works correctly |
| `test_map_temp_to_fahrenheit` | map() + lambda converts temps correctly |
| `test_reduce_total_rainfall` | reduce() + lambda sums rainfall correctly |
| `test_reduce_average_temp` | reduce() + lambda calculates average correctly |
| `test_get_rainfall_by_location` | Groups rainfall by location |
| `test_get_temp_stats_by_location` | Groups temp stats by location |
| `test_str_representation` | __str__ returns expected format |
| `test_repr_representation` | __repr__ returns expected format |
| `test_filter_returns_correct_subset` | Verifies filter() logic |
| `test_map_applies_transformation` | Verifies map() logic |
| `test_reduce_aggregates_correctly` | Verifies reduce() logic |

**Note:** Visual outputs (charts) are tested by inspection, not automated tests.

## Project Structure

```
phase_6/
├── README.md
├── main.py
├── aussie_weather/
│   ├── __init__.py
│   ├── loader.py
│   ├── stats.py
│   ├── writer.py
│   └── visualizer.py      # NEW - visualization & functional programming
├── tests/
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_stats.py
│   ├── test_writer.py
│   └── test_visualizer.py  # NEW - tests for visualizer
└── plots/                   # NEW - saved chart images
    ├── temp_distribution.png
    ├── rainfall_by_location.png
    ├── temp_trends.png
    ├── correlation_heatmap.png
    └── rainy_vs_dry.png
```

## Running the Application

```bash
cd /path/to/PythonDev
source venv/bin/activate
python phase_6/main.py
```

## Running Tests

```bash
cd phase_6
pytest tests/ -v
```

## Dependencies

```bash
pip install matplotlib seaborn
```

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
