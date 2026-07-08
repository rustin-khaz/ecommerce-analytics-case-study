select
    count(*) as total_customers,
    sum(case when lifetime_order_count > 1 then 1 else 0 end) as repeat_customers,
    round(sum(case when lifetime_order_count > 1 then 1 else 0 end)::double / count(*), 4) as repeat_purchase_rate
from {{ ref('dim_customers') }}
