select oi.order_item_id, oi.order_id, o.customer_id, oi.product_id,
       o.order_date::date as order_date, oi.quantity, oi.unit_price,
       (oi.quantity * oi.unit_price)::numeric(12,2) as line_revenue
from {{ ref('stg_order_items') }} oi
join {{ ref('stg_orders') }} o using (order_id)
