select
    is_late_delivery,
    count(*) as order_count,
    round(avg(review_score), 2) as average_review_score
from {{ ref('fct_orders') }}
where review_score is not null
group by 1
