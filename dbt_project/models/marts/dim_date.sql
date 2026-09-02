with bounds as (
  select min(order_date::date) as min_date, max(order_date::date) as max_date
  from {{ ref('stg_orders') }}
), dates as (
  select generate_series(min_date, max_date, interval '1 day')::date as date_day
  from bounds
)
select date_day, extract(year from date_day)::int as year,
       extract(quarter from date_day)::int as quarter,
       extract(month from date_day)::int as month,
       to_char(date_day, 'Month') as month_name,
       extract(isodow from date_day)::int as day_of_week,
       to_char(date_day, 'Day') as day_name,
       extract(isodow from date_day) in (6,7) as is_weekend
from dates
