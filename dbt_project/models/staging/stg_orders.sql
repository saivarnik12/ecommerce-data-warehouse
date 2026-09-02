select order_id, customer_id, order_date, lower(trim(status)) as status,
       shipping_country
from {{ source('raw','orders') }}
