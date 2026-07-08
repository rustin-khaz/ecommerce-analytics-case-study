"""Build the static Plotly dashboard from the KPI warehouse views."""
from pathlib import Path

import duckdb
import pandas as pd
import plotly.graph_objects as go

SURFACE = "#fcfcfb"
BLUE = "#2a78d6"
ORDINAL_RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#184f95"]
GOOD = "#0ca30c"
CRITICAL = "#d03b3b"


def chart_layout(fig, title):
    fig.update_layout(
        title=title,
        plot_bgcolor=SURFACE,
        paper_bgcolor=SURFACE,
        font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color="#0b0b0b"),
        margin=dict(l=60, r=30, t=50, b=40),
    )
    return fig


def build_monthly_gmv_chart(con):
    gmv = con.execute("select * from main.kpi_monthly_gmv order by order_month").fetchdf()
    fig = go.Figure(go.Scatter(
        x=gmv["order_month"], y=gmv["gmv"], mode="lines+markers",
        line=dict(color=BLUE, width=2), marker=dict(size=6),
    ))
    return chart_layout(fig, "Monthly GMV (delivered orders)")


def build_funnel_chart(con):
    funnel = con.execute("select * from main.kpi_order_funnel order by stage_order").fetchdf()
    fig = go.Figure(go.Bar(
        x=funnel["order_count"], y=funnel["stage"], orientation="h",
        marker_color=ORDINAL_RAMP,
        text=[f"{v:.1%}" for v in funnel["pct_of_placed"]], textposition="outside",
    ))
    return chart_layout(fig, "Order funnel")


def build_cohort_heatmap(con):
    cohort = con.execute(
        "select * from main.kpi_cohort_retention where months_since_first_order <= 12"
    ).fetchdf()
    cohort["cohort_month_str"] = cohort["cohort_month"].dt.strftime("%Y-%m")
    pivot = cohort.pivot_table(
        index="cohort_month_str", columns="months_since_first_order", values="retention_rate"
    )
    fig = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale="Blues"))
    return chart_layout(fig, "Cohort retention (first 12 months)")


def build_category_review_chart(con):
    cat = con.execute(
        "select * from main.kpi_review_by_category order by average_review_score desc"
    ).fetchdf()
    top_bottom = pd.concat([cat.head(10), cat.tail(10)])
    fig = go.Figure(go.Bar(
        x=top_bottom["average_review_score"], y=top_bottom["product_category_name_english"],
        orientation="h", marker_color=BLUE,
    ))
    return chart_layout(fig, "Best/worst rated categories (>= 30 orders)")


def build_delivery_speed_chart(con):
    speed = con.execute(
        "select * from main.kpi_review_by_delivery_speed order by is_late_delivery"
    ).fetchdf()
    labels = ["On-time" if not v else "Late" for v in speed["is_late_delivery"]]
    colors = [GOOD if not v else CRITICAL for v in speed["is_late_delivery"]]
    fig = go.Figure(go.Bar(
        x=labels, y=speed["average_review_score"], marker_color=colors,
        text=speed["average_review_score"], textposition="outside",
    ))
    return chart_layout(fig, "Review score by delivery speed")


def build_state_gmv_chart(con):
    state = con.execute("""
        select c.customer_state, round(sum(o.item_revenue),2) as gmv
        from main.fct_orders o
        join main.dim_customers c on o.customer_unique_id = c.customer_unique_id
        where o.order_status = 'delivered'
        group by 1 order by gmv desc limit 10
    """).fetchdf()
    fig = go.Figure(go.Bar(x=state["gmv"], y=state["customer_state"], orientation="h", marker_color=BLUE))
    return chart_layout(fig, "Top 10 states by GMV")


def build_stat_tile(con):
    repeat = con.execute("select * from main.kpi_repeat_purchase_rate").fetchdf().iloc[0]
    return f"""
    <div class="stat-tile">
      <div class="stat-value">{repeat['repeat_purchase_rate']:.1%}</div>
      <div class="stat-label">Repeat purchase rate ({int(repeat['repeat_customers'])} of {int(repeat['total_customers'])} customers)</div>
    </div>
    """


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>E-Commerce Analytics Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  body {{ background: #f9f9f7; font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; margin: 0; padding: 24px; }}
  h1 {{ color: #0b0b0b; }}
  .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; max-width: 1200px; margin: 0 auto; }}
  .chart-card {{ background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 8px; padding: 8px; overflow-x: auto; }}
  .stat-tile {{ grid-column: 1 / -1; background: #fcfcfb; border: 1px solid rgba(11,11,11,0.10); border-radius: 8px; padding: 24px; text-align: center; }}
  .stat-value {{ font-size: 48px; font-weight: 700; color: #2a78d6; }}
  .stat-label {{ color: #52514e; margin-top: 8px; }}
</style>
</head>
<body>
<h1 style="max-width:1200px;margin:0 auto 16px;">E-Commerce Analytics Dashboard</h1>
<div class="grid">
{stat_tile}
<div class="chart-card">{gmv_chart}</div>
<div class="chart-card">{funnel_chart}</div>
<div class="chart-card">{cohort_chart}</div>
<div class="chart-card">{category_chart}</div>
<div class="chart-card">{delivery_chart}</div>
<div class="chart-card">{state_chart}</div>
</div>
</body>
</html>
"""


def main():
    db_path = Path(__file__).resolve().parent.parent / "warehouse" / "olist.duckdb"
    con = duckdb.connect(str(db_path), read_only=True)

    html = PAGE_TEMPLATE.format(
        stat_tile=build_stat_tile(con),
        gmv_chart=build_monthly_gmv_chart(con).to_html(full_html=False, include_plotlyjs=False),
        funnel_chart=build_funnel_chart(con).to_html(full_html=False, include_plotlyjs=False),
        cohort_chart=build_cohort_heatmap(con).to_html(full_html=False, include_plotlyjs=False),
        category_chart=build_category_review_chart(con).to_html(full_html=False, include_plotlyjs=False),
        delivery_chart=build_delivery_speed_chart(con).to_html(full_html=False, include_plotlyjs=False),
        state_chart=build_state_gmv_chart(con).to_html(full_html=False, include_plotlyjs=False),
    )

    out_path = Path(__file__).resolve().parent / "index.html"
    out_path.write_text(html)
    print(f"Dashboard written to {out_path}")
    con.close()


if __name__ == "__main__":
    main()
