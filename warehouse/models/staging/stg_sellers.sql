select
    seller_id,
    seller_zip_code_prefix::varchar as seller_zip_code_prefix,
    seller_city,
    seller_state
from {{ source('raw', 'sellers') }}
qualify row_number() over (partition by seller_id) = 1
