# Australian Weather Data Processor - Phase 4

A Python package for loading, analyzing, and processing Australian weather data, enhanced with functional programming concepts, robust error handling, and logging.

## What's New in Phase 4

This phase builds on the OOP foundation from Phase 3 by adding:

- **Iterators** — `DataFetcher` is now iterable
- **Generators** — `DataProcessor` yields statistics lazily
- **Error Handling** — Try/except blocks with meaningful exceptions
- **Logging** — Application-wide logging for debugging and monitoring

## Iterators

`DataFetcher` now implements `__iter__` and `__next__`, making it iterable over rows:

```python
fetcher = DataFetcher("data/Weather Training Data.csv")
fetcher.load()

for row in fetcher:
    print(row['Location'], row['MaxTemp'])
```

This allows processing data row-by-row without loading everything into memory at once.

## Generators

`DataProcessor.generate_stats()` is a generator that yields statistics one at a time:

```python
processor = DataProcessor(df)

for stat_name, values in processor.generate_stats():
    print(f"{stat_name}: {values.mean()}")
```

**Why use a generator?**
- Memory efficient — calculates each stat on demand
- Flexible — caller can stop early without computing all stats
- Clean — `print_stats()` now uses the generator internally

## Error Handling

Each class validates inputs and handles errors gracefully:

| Class | Errors Handled |
|-------|----------------|
| `DataFetcher` | `FileNotFoundError`, `ValueError` (empty/invalid CSV) |
| `DataProcessor` | `ValueError` (None/empty DataFrame), `TypeError` (wrong type) |
| `DataStorage` | `ValueError` (no path), `IOError` (write failures) |

Example from `loader.py`:
```python
try:
    self._data = pd.read_csv(self.file_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find file: '{self.file_path}'")
except pd.errors.ParserError as e:
    raise ValueError(f"Error parsing CSV: {e}")
```

## Logging

The application uses Python's `logging` module for visibility into execution:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Loaded 99516 records from CSV")
logger.error("File not found: data/missing.csv")
```

**Log levels used:**
- `DEBUG` — Detailed execution steps
- `INFO` — Major milestones (loaded data, wrote file)
- `WARNING` — Non-critical issues (empty columns)
- `ERROR` — Failures that raise exceptions

**Sample output:**
```
2026-01-28 12:00:00 - __main__ - INFO - Starting weather data analysis
2026-01-28 12:00:01 - __main__ - INFO - Loaded 99516 records from CSV
2026-01-28 12:00:02 - __main__ - INFO - Summary written to phase_4/weather_summary.txt
2026-01-28 12:00:02 - __main__ - INFO - Weather data analysis completed successfully
```

## Project Structure

```
phase_4/
├── README.md
├── main.py                     # Entry point with logging config
└── aussie_weather/
    ├── __init__.py             # Package exports
    ├── loader.py               # DataFetcher (iterable, with error handling)
    ├── stats.py                # DataProcessor (generator, with validation)
    └── writer.py               # DataStorage (with error handling)
```

## Running the Application

```bash
cd /path/to/PythonDev
source venv/bin/activate
python phase_4/main.py
```

## Design Choices

1. **Iterator on DataFetcher** — Natural fit for row-by-row processing of large datasets.

2. **Generator for statistics** — Each stat is independent, so yielding them one at a time is more flexible and memory-efficient.

3. **Specific exception types** — Using `FileNotFoundError`, `ValueError`, `IOError` instead of generic `Exception` makes errors easier to catch and handle.

4. **Logging over print** — Logging provides timestamps, levels, and can be configured for different outputs (console, file) without changing code.

5. **Errors logged before re-raising** — Ensures issues are recorded even if the caller doesn't handle them.

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
