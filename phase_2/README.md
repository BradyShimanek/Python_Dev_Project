# Australian Weather Data Processor

A Python package for loading, analyzing, and processing Australian weather data from CSV files.

## Description

This project demonstrates professional Python development practices including:
- Modular package design following PyPA guidelines
- Reading and parsing CSV data using pandas
- Calculating descriptive statistics (mean, median, mode, range, etc.)
- Writing processed data to output files
- Proper code documentation with docstrings
- Publishing packages to TestPyPI

## Dataset

- **Source:** [Kaggle - Australian Weather Data](https://www.kaggle.com/datasets)
- **Records:** 100,000+ weather observations
- **Features:** Temperature, rainfall, humidity, wind speed, and more
- **Format:** CSV files (Training and Test data)

## Installation

### Option 1: Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aussie-weather-sneakytrain
```

### Option 2: Local Development

1. Clone or download this repository

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Installed Package

```python
from aussie_weather import load_weather_data, print_descriptive_stats, write_summary_to_file

# Load the data
df = load_weather_data("path/to/Weather Training Data.csv")

# Print descriptive statistics
print_descriptive_stats(df)

# Write summary to file
write_summary_to_file(df, "output/weather_summary.txt")
```

### Running the Main Script

```bash
cd phase_2
python main.py
```

## Project Structure

```
phase_2/
├── README.md
├── pyproject.toml              # Package configuration
├── main.py                     # Entry point / demo script
└── aussie_weather/             # Package directory
    ├── __init__.py             # Package exports
    ├── loader.py               # Data loading functions
    ├── stats.py                # Descriptive statistics functions
    └── writer.py               # File output functions
```

## Package Functions

| Function | Module | Description |
|----------|--------|-------------|
| `load_weather_data(file_name)` | loader | Load CSV into DataFrame |
| `get_descriptive_stats(df)` | stats | Returns dict with mean, median, mode, range, etc. |
| `print_descriptive_stats(df)` | stats | Prints formatted statistics to console |
| `write_summary_to_file(df, output_file)` | writer | Writes summary report to text file |

## Building & Publishing

### Build the Package

```bash
pip install build twine
python -m build
```

### Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

## Documentation

Generate HTML documentation using pydoc:
```bash
python -m pydoc -w aussie_weather
```

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
