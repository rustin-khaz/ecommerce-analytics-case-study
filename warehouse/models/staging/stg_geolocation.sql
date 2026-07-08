select
    geolocation_zip_code_prefix::varchar as zip_code_prefix,
    geolocation_lat::double as lat,
    geolocation_lng::double as lng,
    geolocation_city as city,
    geolocation_state as state
from {{ source('raw', 'geolocation') }}
