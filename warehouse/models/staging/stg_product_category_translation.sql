select
    product_category_name,
    product_category_name_english
from {{ source('raw', 'product_category_name_translation') }}
qualify row_number() over (partition by product_category_name) = 1
