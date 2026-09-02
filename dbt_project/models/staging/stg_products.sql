select product_id, trim(product_name) as product_name, trim(category) as category,
       price, active
from {{ source('raw','products') }}
