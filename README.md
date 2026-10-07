# E-Commerce Analytics Case Study

I wanted a project that looked like an actual analytics job instead of a single notebook, so I took the [Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (about 99,000 orders from 2016 to 2018) and built the whole thing: a DuckDB warehouse modeled with dbt, KPI views in SQL, a couple of stats notebooks, and a dashboard in Tableau Public.

- [Tableau Public dashboard](https://public.tableau.com/app/profile/rustin.khazravi/viz/OlistE-CommerceAnalytics_17914070197460/OlistE-CommerceRevenueDeliveryandSatisfaction)
- [Full write-up](docs/case_study.md)

[![Tableau dashboard preview](docs/img/dashboard.png)](https://public.tableau.com/app/profile/rustin.khazravi/viz/OlistE-CommerceAnalytics_17914070197460/OlistE-CommerceRevenueDeliveryandSatisfaction)

## What I found

Late deliveries line up with the worst reviews more than anything else I looked at. A late order averages 2.57 stars and an on-time one averages 4.30. I expected that gap to shrink once I controlled for order size, freight cost and state, and it barely moved.

Repeat customers basically don't exist here. Only 3.1% of the 96,096 customers ever placed a second order, so for most people the first order is the whole relationship.

Revenue is lopsided. São Paulo accounts for R$5.07M of the R$13.2M total, almost three times Rio de Janeiro.

Checkout isn't where orders get lost. 99.8% of orders get approved and 97.0% end up delivered, so whatever drop-off there is happens in fulfillment.

The [write-up](docs/case_study.md) goes through the method, what the quasi-experiment can and can't tell you, and what I'd recommend.

## How it fits together

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
   SQL KPI views    Python EDA/stats notebooks       Tableau Public dashboard
  (GMV, AOV, repeat   (EDA, quasi-experiment,        (order-level CSV
   rate, cohort         synthetic RCT module)        export → Tableau)
   retention, funnel)
```

## Repo layout

```
/ingestion      downloads the Kaggle data and loads it into DuckDB (the data itself is gitignored)
/warehouse      dbt project: staging, marts and KPI views
/notebooks      EDA, the quasi-experiment, and a simulated A/B test
/tableau        exports the order-level CSV the Tableau dashboard is built on
/docs           the write-up
```

## Running it yourself

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# pull the dataset and load it into DuckDB
python3 ingestion/download_data.py
python3 ingestion/load_raw.py

# build and test the dbt models
dbt run --project-dir warehouse --profiles-dir warehouse
dbt test --project-dir warehouse --profiles-dir warehouse

# write the CSV that feeds the Tableau dashboard
python3 tableau/export_orders.py

# open the notebooks
jupyter notebook notebooks/
```

`pytest` runs the tests for the download and load steps. The dbt project has 44 data tests of its own (uniqueness, not-null, relationships and so on), which `dbt test` covers.
