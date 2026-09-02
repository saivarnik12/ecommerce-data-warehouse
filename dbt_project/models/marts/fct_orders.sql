with order_totals as (
  select order_id, sum(quantity * unit_price) as order_value, sum(quantity) as item_quantity
  from {{ ref('stg_order_items') }} group by order_id
), paid as (
  select order_id, sum(amount) as paid_amount
  from {{ ref('stg_payments') }} where status = 'paid' group by order_id
)
select o.order_id, o.customer_id, o.order_date, o.status, o.shipping_country,
       coalesce(t.order_value,0)::numeric(12,2) as order_value,
       coalesce(t.item_quantity,0)::int as item_quantity,
       coalesce(p.paid_amount,0)::numeric(12,2) as paid_amount
from {{ ref('stg_orders') }} o
left join order_totals t using (order_id)
left join paid p using (order_id)
