select c.customer_id, c.first_name, c.last_name, c.country,
       count(o.order_id) filter (where o.status <> 'cancelled') as completed_orders,
       coalesce(sum(o.order_value) filter (where o.status <> 'cancelled'),0)::numeric(14,2) as lifetime_value,
       min(o.order_date::date) filter (where o.status <> 'cancelled') as first_order_date,
       max(o.order_date::date) filter (where o.status <> 'cancelled') as last_order_date
from {{ ref('dim_customers') }} c
left join {{ ref('fct_orders') }} o using (customer_id)
group by c.customer_id, c.first_name, c.last_name, c.country
