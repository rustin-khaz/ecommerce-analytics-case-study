with stages as (
    select 'placed' as stage, 1 as stage_order, count(*) as order_count
    from {{ ref('fct_orders') }}

    union all

    select 'approved', 2, sum(case when order_approved_at is not null then 1 else 0 end)
    from {{ ref('fct_orders') }}

    union all

    select 'shipped', 3, sum(case when order_delivered_carrier_at is not null then 1 else 0 end)
    from {{ ref('fct_orders') }}

    union all

    select 'delivered', 4, sum(case when order_delivered_customer_at is not null then 1 else 0 end)
    from {{ ref('fct_orders') }}
)

select
    stage,
    stage_order,
    order_count,
    round(order_count::double / first_value(order_count) over (order by stage_order), 4) as pct_of_placed
from stages
order by stage_order
