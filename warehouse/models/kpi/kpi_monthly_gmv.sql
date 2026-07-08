select
    date_trunc('month', order_purchase_at) as order_month,
    count(*) as order_count,
    round(sum(item_revenue), 2) as gmv,
    round(sum(item_revenue) / count(*), 2) as average_order_value
from {{ ref('fct_orders') }}
where order_status = 'delivered'
group by 1
order by 1
