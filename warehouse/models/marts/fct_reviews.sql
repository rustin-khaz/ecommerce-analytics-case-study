select
    order_id,
    review_id,
    review_score,
    review_created_at
from {{ ref('stg_order_reviews') }}
qualify row_number() over (partition by order_id order by review_created_at desc) = 1
