# Python Development Project

A semester-long Python development project demonstrating professional practices, modular design, and package publishing.

## Dataset

- **Source:** [Kaggle - Australian Weather Data](https://www.kaggle.com/datasets)
- **Records:** 100,000+ weather observations
- **Features:** Temperature, rainfall, humidity, wind speed, and more

## Project Phases

### Phase 1: Environment Setup & File I/O
- Virtual environment configuration
- Git/GitHub source control
- Reading CSV data with pandas
- Writing output to files
- Documentation with pydoc

### Phase 2: Modularization & Package Publishing
- Refactored code into modular package structure
- Descriptive statistics (mean, median, mode, range)
- Built and published package to TestPyPI
- Package: `aussie-weather-sneakytrain`

## Quick Start

```bash
# Clone and setup
git clone https://github.com/BradyShimanek/Python_Dev_Project
cd PythonDev

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aussie-weather-sneakytrain
```

## Project Structure

```
PythonDev/
├── README.md
├── requirements.txt
├── data/                       # Weather CSV files
├── phase_1/                    # Phase 1: Basic script
│   └── aussie_weather.py
└── phase_2/                    # Phase 2: Modular package
    ├── README.md
    ├── pyproject.toml
    ├── main.py
    └── aussie_weather/
        ├── __init__.py
        ├── loader.py
        ├── stats.py
        └── writer.py
```

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
