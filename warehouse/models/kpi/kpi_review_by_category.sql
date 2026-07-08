select
    p.product_category_name_english,
    count(distinct oi.order_id) as order_count,
    round(avg(r.review_score), 2) as average_review_score
from {{ ref('fct_order_items') }} oi
join {{ ref('dim_products') }} p on oi.product_id = p.product_id
join {{ ref('fct_reviews') }} r on oi.order_id = r.order_id
group by 1
having count(distinct oi.order_id) >= 30
order by average_review_score desc
