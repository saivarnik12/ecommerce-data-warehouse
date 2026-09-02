select payment_id, order_id, payment_date, amount, lower(trim(payment_method)) as payment_method,
       lower(trim(status)) as status
from {{ source('raw','payments') }}
