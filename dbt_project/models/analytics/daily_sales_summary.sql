select order_date,
       count(*) filter (where status <> 'cancelled') as orders,
       coalesce(sum(order_value) filter (where status <> 'cancelled'),0)::numeric(14,2) as revenue,
       coalesce(sum(item_quantity) filter (where status <> 'cancelled'),0)::bigint as units_sold
from {{ ref('fct_orders') }}
group by order_date
order by order_date
