select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix::varchar as customer_zip_code_prefix,
    customer_city,
    customer_state
from {{ source('raw', 'customers') }}
qualify row_number() over (partition by customer_id) = 1
