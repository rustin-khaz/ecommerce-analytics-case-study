with orders_per_customer as (
    select
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_at,
        c.customer_city,
        c.customer_state,
        c.customer_zip_code_prefix
    from {{ ref('stg_orders') }} o
    inner join {{ ref('stg_customers') }} c on o.customer_id = c.customer_id
)

select
    customer_unique_id,
    count(distinct order_id) as lifetime_order_count,
    min(order_purchase_at) as first_order_at,
    max(order_purchase_at) as most_recent_order_at,
    arg_max(customer_city, order_purchase_at) as customer_city,
    arg_max(customer_state, order_purchase_at) as customer_state,
    arg_max(customer_zip_code_prefix, order_purchase_at) as customer_zip_code_prefix
from orders_per_customer
group by customer_unique_id
