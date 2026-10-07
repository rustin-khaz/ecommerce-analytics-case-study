"""Export one order-level CSV from the warehouse for the Tableau Public dashboard."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
STATES = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", "CE": "Ceará",
    "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão",
    "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Pará",
    "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima",
    "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}


def main():
    con = duckdb.connect(str(ROOT / "warehouse" / "olist.duckdb"), read_only=True)
    con.execute("create temp table states (code varchar, name varchar)")
    con.executemany("insert into states values (?, ?)", list(STATES.items()))
    out = ROOT / "tableau" / "orders.csv"
    con.execute(f"""
        copy (
          select o.customer_unique_id as customer_id, o.order_status,
                 o.order_purchase_at::date as purchase_date, 'Brazil' as country, s.name as state,
                 coalesce(replace(p.product_category_name_english, '_', ' '), 'unknown') as category,
                 o.item_count, o.item_revenue, o.freight_total, o.review_score,
                 least(o.delivery_days, 40) as delivery_days_capped,
                 o.is_late_delivery::int as is_late,
                 (c.lifetime_order_count > 1)::int as is_repeat_customer
          from main.fct_orders o
          join main.dim_customers c using (customer_unique_id)
          join states s on s.code = c.customer_state
          left join (select order_id, product_id from main.fct_order_items where order_item_id = 1) i
            using (order_id)
          left join main.dim_products p using (product_id)
        ) to '{out}' (header)
    """)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
