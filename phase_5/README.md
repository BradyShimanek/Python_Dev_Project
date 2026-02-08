# Australian Weather Data Processor - Phase 5

A Python package for loading, analyzing, and processing Australian weather data, with comprehensive unit testing.

## What's New in Phase 5

This phase adds automated unit testing using Python's `unittest` framework:

- **38 test cases** covering all three classes
- **Test fixtures** with temporary files and sample data
- **Mocking** for error condition testing
- **Coverage testing** to ensure all code is executed

## Running the Tests

```bash
cd /path/to/PythonDev/phase_5

# Run all tests
python -m unittest discover -s tests -v

# Run tests for a specific module
python -m unittest tests.test_loader -v
python -m unittest tests.test_stats -v
python -m unittest tests.test_writer -v
```

## Coverage Testing

```bash
# Install coverage (if not installed)
pip install coverage

# Run tests with coverage
coverage run -m unittest discover -s tests

# View coverage report
coverage report -m

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Test Cases

### DataFetcher Tests (test_loader.py)

| Test Case | Description |
|-----------|-------------|
| `test_load_valid_csv` | Successfully loads a valid CSV file |
| `test_load_file_not_found` | Raises `FileNotFoundError` for missing file |
| `test_load_empty_file` | Raises `ValueError` for empty CSV |
| `test_data_property_lazy_loads` | Data property triggers lazy loading |
| `test_record_count` | Returns correct number of records |
| `test_columns` | Returns correct column names |
| `test_iterator` | Class is iterable over rows |
| `test_iterator_resets` | Iterator resets on each new iteration |
| `test_str_representation` | `__str__` returns expected format |
| `test_repr_representation` | `__repr__` returns expected format |

### DataProcessor Tests (test_stats.py)

| Test Case | Description |
|-----------|-------------|
| `test_init_valid_dataframe` | Initializes with valid DataFrame |
| `test_init_none_raises_value_error` | Raises `ValueError` for None input |
| `test_init_wrong_type_raises_type_error` | Raises `TypeError` for non-DataFrame |
| `test_init_empty_dataframe_raises_value_error` | Raises `ValueError` for empty DataFrame |
| `test_numeric_data_filters_correctly` | Filters to only numeric columns |
| `test_generate_stats_yields_all_stats` | Generator yields all 8 statistics |
| `test_generate_stats_is_generator` | Returns a generator object |
| `test_stats_property_returns_dict` | Stats property returns dictionary |
| `test_stats_property_caches_result` | Stats are cached after first calculation |
| `test_mean_calculation` | Mean is calculated correctly |
| `test_median_calculation` | Median is calculated correctly |
| `test_min_max_calculation` | Min and max are calculated correctly |
| `test_range_calculation` | Range (max - min) is calculated correctly |
| `test_str_representation` | `__str__` returns expected format |
| `test_repr_representation` | `__repr__` returns expected format |

### DataStorage Tests (test_writer.py)

| Test Case | Description |
|-----------|-------------|
| `test_init_with_dataframe` | Initializes with DataFrame |
| `test_init_with_output_path` | Initializes with DataFrame and path |
| `test_write_summary_success` | Successfully writes file |
| `test_write_summary_with_override_path` | Writes to overridden path |
| `test_write_summary_no_path_raises` | Raises `ValueError` when no path |
| `test_write_summary_content_header` | File contains expected header |
| `test_write_summary_content_record_count` | File contains record count |
| `test_write_summary_content_columns` | File contains column names |
| `test_write_summary_content_statistics` | File contains statistics |
| `test_write_summary_permission_error` | Raises `IOError` on permission denied |
| `test_str_representation` | `__str__` returns expected format |
| `test_repr_representation` | `__repr__` returns expected format |

## Test Design Principles

1. **Isolation** — Each test is independent and cleans up after itself
2. **Fixtures** — `setUp()` creates test data, `tearDown()` removes it
3. **Mocking** — Uses `unittest.mock` to simulate error conditions
4. **Temporary Files** — Uses `tempfile` for safe file operations
5. **Assertions** — Tests use specific assertions (`assertEqual`, `assertRaises`, etc.)

## Project Structure

```
phase_5/
├── README.md
├── main.py
├── aussie_weather/
│   ├── __init__.py
│   ├── loader.py
│   ├── stats.py
│   └── writer.py
└── tests/
    ├── __init__.py
    ├── test_loader.py      # 10 tests for DataFetcher
    ├── test_stats.py       # 16 tests for DataProcessor
    └── test_writer.py      # 12 tests for DataStorage
```

## Author

Brady S  
Python Development - Spring 2026  
Utah Valley University

## Acknowledgments

- Weather dataset from [Kaggle](https://www.kaggle.com/datasets)
- AI assistance was used for documentation generation
