select date_trunc('month', oi.order_date)::date as month_start,
       p.category,
       sum(oi.line_revenue)::numeric(14,2) as revenue,
       sum(oi.quantity)::bigint as units_sold
from {{ ref('fct_order_items') }} oi
join {{ ref('dim_products') }} p using (product_id)
join {{ ref('fct_orders') }} o using (order_id)
where o.status <> 'cancelled'
group by 1, 2
order by 1, 2
