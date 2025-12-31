# Australian Weather Data Processor

A Python application that reads, processes, and analyzes Australian weather data from CSV files.

## Description

This project demonstrates professional Python development practices including:
- Reading and parsing CSV data using pandas
- Storing data in Python data structures
- Writing processed data to output files
- Proper code documentation with docstrings
- Virtual environment setup and dependency management

## Setup

### Prerequisites
- Python 3.x installed on your system

### Installation

1. Clone or download this repository

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure your virtual environment is activated (you should see `(venv)` in your terminal prompt)

2. Run the main script:
   ```bash
   python phase_1/aussie_weather.py
   ```

3. The program will:
   - Load weather data from `data/Weather Training Data.csv`
   - Display the number of records and statistical summary
   - Generate a summary report at `data/weather_summary.txt`

## Project Structure

```
PythonDev/
├── README.md
├── requirements.txt
├── venv/                          # Virtual environment (not tracked in git)
├── data/
│   ├── Weather Training Data.csv  # Input data
│   └── weather_summary.txt        # Generated summary output
└── phase_1/
    └── aussie_weather.py          # Main application script
```

## Documentation

To generate HTML documentation using pydoc:
```bash
python -m pydoc -w phase_1.aussie_weather
```

This creates `phase_1.aussie_weather.html` which can be viewed in any web browser.

## Author

Brady Shimanek  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
