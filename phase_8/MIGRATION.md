# Migration to PySpark Cluster

This document describes considerations and changes made to run the Aussie Weather pipeline on a PySpark cluster (Google Colab).

---

## Considerations

| Consideration | Notes |
|--------------|--------|
| **Execution environment** | The original app assumed a local Python process with pandas. On a cluster, the driver runs in Colab and Spark distributes work across executors. Code was updated to assume a SparkSession and use Spark APIs for data. |
| **Data loading** | Pandas `read_csv` loads into a single process. For cluster parallelism, data is loaded with `spark.read.csv()` into a Spark DataFrame so it can be partitioned and processed on executors. |
| **Lazy evaluation** | Spark DataFrames are lazy: transformations (filter, select, groupBy) build a DAG; nothing runs until an action (count, collect, show, write). Actions are used only where results are needed (e.g. count, collect, toPandas). |
| **Where to collect** | Bringing data to the driver (e.g. `.collect()`, `.toPandas()`) is expensive and can OOM. Collection is limited to: small aggregates for printing, the summary file, and plot inputs. Heavy filtering and aggregation stay in Spark. |
| **Plotting** | Spark does not provide matplotlib. Plotting is done on the driver: run aggregations in Spark, then `.toPandas()` or `.collect()` only the small result (e.g. one row per location, or a 1000-row sample), then use pandas + matplotlib/seaborn on the driver. |
| **File paths in Colab** | Colab’s filesystem differs from local. Outputs use `/content/` for the uploaded CSV and for written artifacts (e.g. `/content/weather_summary.txt`, `/content/plots/`). The CSV is uploaded once via `google.colab.files.upload()`. |
| **Stats parity** | The previous local pipeline used mean, median, mode, std, min, max, range, count. Spark provides `describe()` for count/mean/stddev/min/max. Median is implemented with `approxQuantile()`; mode was omitted (could be added via groupBy + count per column). |

---

## Changes Made

| Component | Before (local) | After (PySpark / Colab) |
|----------|-----------------|--------------------------|
| **Session** | No Spark; async + multiprocessing in one process. | Install PySpark; create `SparkSession` with `SparkSession.builder.appName(...).getOrCreate()`. |
| **Data load** | `DataFetcher` + pandas `read_csv` (async in thread). | `spark.read.option("header", True).option("inferSchema", True).csv(csv_path)`; DataFrame is distributed. |
| **Record count / columns** | `len(df)`, `df.columns`. | `df.count()`, `df.columns` (count is an action; columns is metadata). |
| **Descriptive stats** | Pandas `DataProcessor`: mean, median, mode, std, min, max, range, count. | Spark `df.select(numeric_cols).describe()` for summary; `df.approxQuantile(col, [0.5], 0.01)` for median. |
| **Summary file** | Pandas `describe()` written to file from main process. | `desc.toPandas()` then write the same summary text to `/content/weather_summary.txt` from the driver. |
| **Filter rainy / hot** | Pandas `df[df['Rainfall'] > 0]`, `df[df['MaxTemp'] > 35]`. | Spark `df.filter(F.col("Rainfall") > 0)`, `df.filter(F.col("MaxTemp") > 35)`; `.count()` to get counts. |
| **Map to Fahrenheit** | Pandas column * 9/5 + 32. | Spark `df.select((F.col("MaxTemp") * 9/5 + 32).alias("MaxTemp_F"))`, then `.limit(3).collect()` for sample. |
| **Total rainfall / avg temp** | Pandas `sum`, `mean`. | Spark `df.agg(F.sum(F.coalesce("Rainfall", 0)))`, `df.agg(F.avg("MaxTemp"))`, then `.collect()[0][0]`. |
| **Rainfall by location** | Pandas `groupby('Location')['Rainfall'].mean().sort_values(ascending=False)`. | Spark `df.groupBy("Location").agg(F.avg("Rainfall")).orderBy(F.desc("avg_rain")).limit(5)`, then `.collect()`. |
| **Plots** | Matplotlib/seaborn on pandas DataFrames in the main process (or worker processes in the local version). | For each plot: get data from Spark (e.g. `df.select(...).toPandas()` or aggregated `.toPandas()`), then matplotlib/seaborn on the driver; save to `/content/plots/*.png`. |
| **Package layout** | Local package `aussie_weather` with loader, stats, writer, visualizer. | Single Colab notebook using PySpark and driver-side pandas/matplotlib; no local package import. |

---

## How to Run

1. Open [Google Colab](https://colab.research.google.com).
2. Upload the notebook `phase_8_pyspark.ipynb` (File → Upload notebook).
3. Run all cells in order. When prompted, upload the weather CSV used by the local pipeline.
4. Summary and plots are written under `/content/`.

Colab’s runtime provides the Spark session (virtual cluster); no paid accounts or external clusters are required.
