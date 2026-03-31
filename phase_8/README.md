# Australian Weather Data Processor - Phase 8

Phase 8 runs the same weather analysis on a **PySpark cluster** (Google Colab). Data loading, stats, and aggregations use Spark; plots are generated on the driver from Spark results.

## What Was Done

- **PySpark session:** Notebook installs PySpark and creates a `SparkSession` (Part 1 style).
- **Data load:** CSV is read with `spark.read.csv()` into a Spark DataFrame (distributed).
- **Stats:** Descriptive statistics via Spark `describe()` and `approxQuantile()` for median.
- **Summary file:** Spark summary is collected to the driver and written to `/content/weather_summary.txt`.
- **Filter / map / reduce:** Implemented with Spark `filter()`, `select()`, `agg()`, `groupBy()`.
- **Plots:** Spark produces the aggregated/sampled data; results are collected with `.toPandas()` and plotted with matplotlib/seaborn on the driver; images saved under `/content/plots/`.

Details on design choices and code changes are in **MIGRATION.md**.

## How to Run (Google Colab)

1. Open [Google Colab](https://colab.research.google.com).
2. **File → Upload notebook** and select `phase_8_pyspark.ipynb`.
3. Run all cells in order. When prompted, upload **Weather Training Data.csv** (same file as phase_6/phase_7).
4. Outputs: `/content/weather_summary.txt` and `/content/plots/*.png`. Take **multiple screenshots** of a successful, error-free run for submission.

No paid accounts; Colab’s free runtime is enough.

## Changes Made for PySpark

| Area | Change |
|------|--------|
| Environment | Single Colab notebook; no local `aussie_weather` package in the notebook. |
| Data source | CSV uploaded in Colab; path set to `/content/<filename>`. |
| Load | `spark.read.option("header", True).option("inferSchema", True).csv(path)` instead of pandas `read_csv`. |
| Stats | Spark `describe()` + `approxQuantile()` for median; no pandas `DataProcessor`. |
| Filter/aggregate | Spark `filter()`, `agg()`, `groupBy()`, `orderBy()`; results brought to driver only when needed. |
| Plots | Spark builds aggregates/samples; `.toPandas()` or `.collect()` on small results; matplotlib/seaborn on driver; save to `/content/plots/`. |

See **MIGRATION.md** for full considerations and before/after comparison.

## Project Structure

```
phase_8/
├── README.md
├── MIGRATION.md           # What we considered and changed for PySpark
├── phase_8_pyspark.ipynb  # Colab notebook – upload this and run
├── aussie_weather/        # (Unchanged from phase_7; not used by the notebook)
├── tests/
└── ...
```

## Submission

- **Zip:** Code + README + MIGRATION.md (and notebook). No screenshots in the zip.
- **Screenshots:** Submit separately; multiple screenshots showing successful, error-free execution.

## Author

Brady S — Python Development, Spring 2026, UVU

### Acknowledgements
- AI was used to assist in the development of this documentation
