with item_agg as (
    select
        order_id,
        count(*) as item_count,
        sum(price) as item_revenue,
        sum(freight_value) as freight_total
    from {{ ref('fct_order_items') }}
    group by order_id
)

select
    o.order_id,
    c.customer_unique_id,
    o.order_status,
    o.order_purchase_at,
    o.order_approved_at,
    o.order_delivered_carrier_at,
    o.order_delivered_customer_at,
    o.order_estimated_delivery_at,
    coalesce(i.item_count, 0) as item_count,
    coalesce(i.item_revenue, 0) as item_revenue,
    coalesce(i.freight_total, 0) as freight_total,
    coalesce(i.item_revenue, 0) + coalesce(i.freight_total, 0) as order_total,
    coalesce(p.total_payment_value, 0) as total_payment_value,
    r.review_score,
    datediff('day', o.order_purchase_at, o.order_delivered_customer_at) as delivery_days,
    case
        when o.order_delivered_customer_at is not null
             and o.order_delivered_customer_at > o.order_estimated_delivery_at
        then true
        else false
    end as is_late_delivery
from {{ ref('stg_orders') }} o
inner join {{ ref('stg_customers') }} c on o.customer_id = c.customer_id
left join item_agg i on o.order_id = i.order_id
left join {{ ref('fct_payments') }} p on o.order_id = p.order_id
left join {{ ref('fct_reviews') }} r on o.order_id = r.order_id
