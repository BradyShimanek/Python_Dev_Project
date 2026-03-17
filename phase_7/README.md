# Australian Weather Data Processor - Phase 7

Same behavior as Phase 6, with async data loading and multiprocessing for compute-heavy work.

## What's new in Phase 7:

- **Async I/O:** CSV loading runs in a thread pool via `asyncio.to_thread()` so the event loop is not blocked.
- **Multiprocessing:** Descriptive statistics and all five plot generations run in a `multiprocessing.Pool` (6 workers: 1 stats + 5 plots) for multi-core use.
- Output (summary file, plots, console stats and functional examples) is unchanged from the sequential version.

Run from project root with venv active:

```bash
source venv/bin/activate
python phase_7/main.py
```

---

## Where Asynchronous Features Are Used

| Location | Feature | Why |
|----------|---------|-----|
| `main.py` | `asyncio.run(load_data_async())` | Entry point that runs the async load. |
| `aussie_weather/loader.py` | `DataFetcher.load_async()` | Non-blocking load: runs `pd.read_csv()` in a thread via `asyncio.to_thread(self.load)` so the event loop can do other work during I/O. Data loading is I/O-bound. |

---

## Where Parallelism (Multiprocessing) Is Used

| Location | Feature | Why |
|----------|---------|-----|
| `main.py` | `multiprocessing.Pool(6)` | One pool for all CPU-bound tasks. |
| `main.py` | `pool.apply_async(compute_stats_string, (df,))` | Stats run in a separate process so the main process is not blocked; stats are CPU-bound. |
| `main.py` | `pool.map(generate_plot, plot_args)` | Each of the 5 plots is generated in its own process so multiple cores are used; plot generation is CPU-bound. |
| `aussie_weather/stats.py` | `compute_stats_string(df)` | Top-level function run in a worker; computes descriptive statistics and returns a formatted string. |
| `aussie_weather/visualizer.py` | `generate_plot(args)` | Top-level worker: given `(plot_name, df, save_path)`, builds one plot and saves to disk. |

---

## Automated Test Cases

Phase 7 reuses the same tests as Phase 6 (package behavior is unchanged). Run from project root:

```bash
source venv/bin/activate
pytest phase_7/tests/ -v
```

| Test module | Test cases |
|-------------|------------|
| **test_loader.py** | `test_init`, `test_load_success`, `test_load_file_not_found`, `test_load_empty_raises`, `test_data_property`, `test_record_count`, `test_columns`, `test_iteration`, `test_str_repr` |
| **test_stats.py** | `test_init_valid`, `test_init_none_raises`, `test_init_empty_raises`, `test_numeric_data`, `test_stats_property`, `test_generate_stats`, `test_compute_stats_string`, `test_str_repr` |
| **test_writer.py** | `test_init`, `test_write_summary_returns_path`, `test_write_summary_content`, `test_write_summary_no_path_raises`, `test_str_repr` |
| **test_visualizer.py** | `test_init_valid_dataframe`, `test_init_none_raises`, `test_init_empty_raises`, `test_filter_rainy_days`, `test_filter_hot_days`, `test_filter_hot_days_custom_threshold`, `test_map_temp_to_fahrenheit`, `test_reduce_total_rainfall`, `test_reduce_average_temp`, `test_get_rainfall_by_location`, `test_get_temp_stats_by_location`, `test_str_repr`, `test_repr_representation`, `test_filter_returns_correct_subset`, `test_map_applies_transformation`, `test_reduce_aggregates_correctly` |

(Exact test names may vary slightly; run `pytest phase_7/tests/ -v --collect-only` to list them.)

---

## Project Structure

```
phase_7/
├── README.md
├── main.py                 # Async load + multiprocessing orchestration
├── aussie_weather/
│   ├── __init__.py
│   ├── loader.py           # DataFetcher + load_async()
│   ├── stats.py            # DataProcessor + compute_stats_string()
│   ├── writer.py
│   └── visualizer.py       # DataVisualizer + generate_plot() worker
├── tests/
│   ├── test_loader.py
│   ├── test_stats.py
│   ├── test_writer.py
│   └── test_visualizer.py
└── plots/
    └── (generated PNGs)
```

---

## Dependencies

Same as Phase 6: pandas, matplotlib, seaborn (and project venv).

---

## Author

Brady S — Python Development, Spring 2026, UVU
