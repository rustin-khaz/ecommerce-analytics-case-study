select
    order_id,
    sum(payment_value) as total_payment_value,
    count(*) as payment_count,
    max(payment_installments) as max_installments,
    arg_min(payment_type, payment_sequential) as primary_payment_type
from {{ ref('stg_order_payments') }}
group by order_id
