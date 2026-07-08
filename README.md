# E-Commerce Analytics Case Study

An end-to-end analytics case study on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce):
ingestion, warehouse modeling, business KPIs, causal/experiment analysis,
a live dashboard, and a written case study.

- **[Live dashboard](https://rustin-khaz.github.io/ecommerce-analytics-case-study/dashboard/)**
- **[Case study write-up](docs/case_study.md)**

## Architecture

```
Kaggle CSVs → Python ingestion script → DuckDB (raw schema)
                                            │
                                    dbt-core models
                                            │
                        staging (cleaned, typed, deduped)
                                            │
                mart layer: dim_customers, dim_products, fct_orders,
                fct_order_items, fct_payments, fct_reviews
                                            │
        ┌───────────────┬──────────────────┴───────────────┐
   SQL KPI views    Python EDA/stats notebooks         Plotly dashboard
  (GMV, AOV, repeat   (EDA, quasi-experiment,          (published via
   rate, cohort         synthetic RCT module)          GitHub Pages)
   retention, funnel)
```

## Repo Structure

```
/ingestion      Kaggle download script + DuckDB raw loader (data itself is gitignored)
/warehouse      dbt project (staging + marts + KPI views)
/notebooks      EDA, quasi-experiment, synthetic RCT
/dashboard      Plotly dashboard build script + generated HTML (live via GitHub Pages)
/docs           case study write-up
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download the dataset and load it into the DuckDB warehouse
python3 ingestion/download_data.py
python3 ingestion/load_raw.py

# Build the dbt staging/mart/KPI layers
dbt run --project-dir warehouse --profiles-dir warehouse
dbt test --project-dir warehouse --profiles-dir warehouse

# Rebuild the dashboard from the current warehouse
python3 dashboard/build_dashboard.py

# Run the notebooks (EDA, quasi-experiment, synthetic RCT)
jupyter notebook notebooks/
```

Run `pytest` to check the ingestion test suite (dataset download, raw loader).
