# Australian Weather Data Processor - Phase 3

A Python package for loading, analyzing, and processing Australian weather data, refactored with class-based architecture.

## Design Overview

Phase 3 refactors the functional code from Phase 2 into a class-based design. Each major responsibility is encapsulated in its own class:

| Class | Responsibility |
|-------|----------------|
| `DataFetcher` | Loading weather data from CSV files |
| `DataProcessor` | Calculating descriptive statistics |
| `DataStorage` | Writing summaries to output files |

## OOP Principles Applied

### Encapsulation

Each class bundles related data and behavior together. Internal state is protected using underscore-prefixed attributes:

```python
class DataFetcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self._data = None  # Internal state
```

### Properties

The `@property` decorator provides controlled access to internal data with lazy loading:

```python
@property
def data(self):
    if self._data is None:
        self.load()
    return self._data
```

This pattern is used for:
- `DataFetcher.data`, `DataFetcher.record_count`, `DataFetcher.columns`
- `DataProcessor.stats`, `DataProcessor.numeric_data`

### Dunder Methods

Each class implements special methods for better usability:

- `__init__` — Constructor for initialization
- `__str__` — Human-readable string representation
- `__repr__` — Developer-friendly representation

```python
def __str__(self):
    return f"DataFetcher(file='{self.file_path}', records={self.record_count})"
```

### Lazy Evaluation

Statistics and data are only calculated when first accessed, improving performance:

```python
@property
def stats(self):
    if self._stats is None:
        self._stats = self._calculate_stats()
    return self._stats
```

## Project Structure

```
phase_3/
├── README.md
├── main.py                     # Entry point
└── aussie_weather/
    ├── __init__.py             # Package exports
    ├── loader.py               # DataFetcher class
    ├── stats.py                # DataProcessor class
    └── writer.py               # DataStorage class
```

## Usage

```python
from aussie_weather import DataFetcher, DataProcessor, DataStorage

# Load data
fetcher = DataFetcher("data/Weather Training Data.csv")
fetcher.load()
print(fetcher)  # DataFetcher(file='...', records=100000)

# Process statistics
processor = DataProcessor(fetcher.data)
processor.print_stats()

# Save summary
storage = DataStorage(fetcher.data, "output/summary.txt")
storage.write_summary()
```

## Running the Application

```bash
cd /path/to/PythonDev
source venv/bin/activate
python phase_3/main.py
```

## Design Choices

1. **Separate classes for each concern** — Follows single responsibility principle. Each class does one thing well.

2. **Properties over direct attribute access** — Allows validation, lazy loading, and future flexibility without changing the interface.

3. **Lazy loading pattern** — Data and statistics are computed only when needed, not at initialization.

4. **Consistent dunder methods** — All classes have `__str__` and `__repr__` for debugging and logging.

5. **Optional parameters with defaults** — `DataStorage` accepts an optional `output_path` that can be overridden in `write_summary()`.

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
