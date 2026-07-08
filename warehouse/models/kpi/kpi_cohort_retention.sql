with cohort as (
    select
        customer_unique_id,
        date_trunc('month', first_order_at) as cohort_month
    from {{ ref('dim_customers') }}
),

cohort_size as (
    select cohort_month, count(distinct customer_unique_id) as cohort_customers
    from cohort
    group by 1
),

activity as (
    select
        c.customer_unique_id,
        c.cohort_month,
        date_diff('month', c.cohort_month, date_trunc('month', o.order_purchase_at)) as months_since_first_order
    from cohort c
    join {{ ref('fct_orders') }} o on c.customer_unique_id = o.customer_unique_id
)

select
    a.cohort_month,
    a.months_since_first_order,
    count(distinct a.customer_unique_id) as active_customers,
    s.cohort_customers,
    round(count(distinct a.customer_unique_id)::double / s.cohort_customers, 4) as retention_rate
from activity a
join cohort_size s on a.cohort_month = s.cohort_month
group by 1, 2, 4
order by 1, 2
